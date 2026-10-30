#!/usr/bin/env bash
#
# Render checks for the verify-image-signatures ImageValidatingPolicy family.
#
# Renders the chart with a series of values files and asserts the result with
# yq (mikefarah v4). Stops at the first failed assertion. Needs only helm, yq
# and bash. Values files are written to a temporary directory that is removed
# on exit. Rendered manifests are passed to yq on stdin, because a snap-packaged
# yq cannot read files under /tmp.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
chart="${repo_root}/helm/kyverno-policies"
schema="${chart}/values.schema.json"

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT

# A throwaway public key, only used to give key-based attestors a valid shape.
read -r -d '' pubkey <<'KEY' || true
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE4h7OqaHGFIiKU9bHkoIGEtyWx6ZY
2cyW9dBFyAqV46pa8zojEovfo18bnQ1FZKB1gA2wvq1+gwvsMhNLIuS+5w==
-----END PUBLIC KEY-----
KEY
indented_key="$(printf '%s\n' "${pubkey}" | sed 's/^/              /')"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

ok() {
  echo "ok   $*"
}

# render <values-file> prints the ImageValidatingPolicy documents of the chart
# rendered with that values file (empty file name: chart defaults).
render() {
  local out
  if [ -n "${1:-}" ]; then
    out="$(helm template kp "${chart}" -f "$1" 2>&1)" || fail "helm template with $1 failed: ${out}"
  else
    out="$(helm template kp "${chart}" 2>&1)" || fail "helm template with default values failed: ${out}"
  fi
  printf '%s\n' "${out}" | yq 'select(.kind == "ImageValidatingPolicy")'
}

# q <rendered> <expr> evaluates a yq expression on the rendered policies and
# prints the result as compact JSON (strings stay quoted).
q() {
  printf '%s\n' "$1" | yq -o=json -I=0 "$2"
}

# policy_raw <name> <expr> is policy with the result printed as a plain string.
policy_raw() {
  printf '%s\n' "${RENDERED}" | yq -r "select(.metadata.name == \"$1\") | $2"
}

# names <rendered> prints the policy names as compact JSON, in render order.
names() {
  printf '%s\n' "$1" | yq ea -o=json -I=0 '[.metadata.name]'
}

# expect <what> <actual> <expected> compares two strings.
expect() {
  if [ "$2" != "$3" ]; then
    fail "$1: expected $3, got $2"
  fi
}

# policy <name> <expr> evaluates expr on the one policy of that name.
policy() {
  q "${RENDERED}" "select(.metadata.name == \"$1\") | $2"
}

# Common values fragments.
customer_acme() {
  cat <<YAML
imageVerification:
  customer:
    - name: acme
      images: ["*/*"]
      attestors:
        - name: ci
          key:
            publicKey: |
${indented_key}
          ignoreTlog: true
YAML
}

default_name="verify-image-signatures-gsoci-circleci-keyless"
default_attestors='[{"name":"circleci","cosign":{"keyless":{"identities":[{"issuer":"https://oidc.circleci.com","subjectRegExp":"^https://circleci\\.com/api/v2/projects/[a-f0-9-]+/pipeline-definitions/([a-f0-9-]+|nil)$"}]},"ctlog":{"url":"https://rekor.sigstore.dev","insecureIgnoreTlog":false}}}]'

# 1. Defaults ---------------------------------------------------------------
RENDERED="$(render "")"
expect "default: policy names" "$(names "${RENDERED}")" "[\"${default_name}\"]"
expect "default: validationActions" "$(policy "${default_name}" '.spec.validationActions')" '["Audit"]'
expect "default: admission.enabled" "$(policy "${default_name}" '.spec.evaluation.admission.enabled')" 'false'
expect "default: failurePolicy" "$(policy "${default_name}" '.spec.failurePolicy')" '"Ignore"'
expect "default: mutateDigest" "$(policy "${default_name}" '.spec.validationConfigurations.mutateDigest')" 'false'
expect "default: attestor names" "$(policy "${default_name}" '[.spec.attestors[].name]')" '["circleci"]'
expect "default: CEL ends in e >= 1" "$(policy "${default_name}" '.spec.validations[0].expression | test("e >= 1\\)$")')" 'true'
ok "default render: one policy ${default_name}, Audit, admission off, failurePolicy Ignore, mutateDigest off, attestor circleci, e >= 1"

# 2. Customer entry -----------------------------------------------------------
customer_acme >"${tmp}/customer.yaml"
RENDERED="$(render "${tmp}/customer.yaml")"
expect "customer: policy names" "$(names "${RENDERED}")" "[\"${default_name}\",\"verify-image-signatures-acme\"]"
exclusion='!["^gsoci\\.azurecr\\.io/giantswarm/.*$"].exists(p, ref.matches(p))'
expr="$(policy_raw verify-image-signatures-acme '.spec.matchImageReferences[0].expression')"
case "${expr}" in
  *"${exclusion}"*) ;;
  *) fail "customer: acme matchImageReferences[0].expression lacks the negated gsoci.azurecr.io/giantswarm/* regex: ${expr}" ;;
esac
expect "customer: acme key.data is set" "$(policy verify-image-signatures-acme '.spec.attestors[0].cosign.key.data | test("BEGIN PUBLIC KEY")')" 'true'
expect "customer: acme has no keyless" "$(policy verify-image-signatures-acme '.spec.attestors[0].cosign | has("keyless")')" 'false'
ok "customer entry: two policies, acme excludes gsoci.azurecr.io/giantswarm/*, key attestor without keyless"

# 3. Customer entry, Giant Swarm verifier disabled ---------------------------
{
  customer_acme
  cat <<'YAML'
  giantswarm:
    gsoci-circleci-keyless:
      enabled: false
YAML
} >"${tmp}/customer-gs-disabled.yaml"
RENDERED="$(render "${tmp}/customer-gs-disabled.yaml")"
expect "gs disabled: policy names" "$(names "${RENDERED}")" '["verify-image-signatures-acme"]'
expect "gs disabled: acme has no exclusion expression" "$(policy verify-image-signatures-acme '[.spec.matchImageReferences[] | select(has("expression"))] | length')" '0'
expect "gs disabled: acme match" "$(policy verify-image-signatures-acme '.spec.matchImageReferences')" '[{"glob":"*/*"}]'
ok "giantswarm verifier disabled: only verify-image-signatures-acme, no exclusion in its match"

# 4. Enforce mode ---------------------------------------------------------------
cat >"${tmp}/enforce.yaml" <<'YAML'
imageVerification:
  giantswarm:
    gsoci-circleci-keyless:
      mode: Enforce
YAML
RENDERED="$(render "${tmp}/enforce.yaml")"
expect "enforce: policy names" "$(names "${RENDERED}")" "[\"${default_name}\"]"
expect "enforce: validationActions" "$(policy "${default_name}" '.spec.validationActions')" '["Deny"]'
expect "enforce: admission.enabled" "$(policy "${default_name}" '.spec.evaluation.admission.enabled')" 'true'
expect "enforce: failurePolicy" "$(policy "${default_name}" '.spec.failurePolicy')" '"Ignore"'
expect "enforce: attestors" "$(policy "${default_name}" '.spec.attestors')" "${default_attestors}"
ok "mode Enforce alone: [Deny], admission on, failurePolicy Ignore, attestors unchanged"

# 5. Two attestors, two required -------------------------------------------------
cat >"${tmp}/two-attestors.yaml" <<YAML
imageVerification:
  giantswarm:
    gsoci-circleci-keyless:
      minVerifiedAttestors: 2
      attestors:
        - name: circleci
          keyless:
            issuer: https://oidc.circleci.com
            subjectRegExp: ^https://circleci\.com/api/v2/projects/[a-f0-9-]+/pipeline-definitions/([a-f0-9-]+|nil)\$
          rekorUrl: https://rekor.sigstore.dev
          ignoreTlog: false
        - name: kms
          key:
            publicKey: |
${indented_key}
          ignoreTlog: true
YAML
RENDERED="$(render "${tmp}/two-attestors.yaml")"
expect "two attestors: policy names" "$(names "${RENDERED}")" "[\"${default_name}\"]"
expect "two attestors: attestor names" "$(policy "${default_name}" '[.spec.attestors[].name]')" '["circleci","kms"]'
expect "two attestors: CEL ends in e >= 2" "$(policy "${default_name}" '.spec.validations[0].expression | test("e >= 2\\)$")')" 'true'
expect "two attestors: CEL lists both attestors" "$(policy "${default_name}" '.spec.validations[0].expression | test("\\[attestors\\.circleci, attestors\\.kms\\]")')" 'true'
ok "attestors overridden: two attestors rendered, CEL ends in e >= 2"

# 6. policyNamePrefix ------------------------------------------------------------
cat >"${tmp}/prefix.yaml" <<YAML
policyNamePrefix: gs-
imageVerification:
  customer:
    - name: my-corp
      images: ["registry.example/my-corp/*"]
      attestors:
        - name: ci
          key:
            publicKey: |
${indented_key}
          ignoreTlog: true
YAML
RENDERED="$(render "${tmp}/prefix.yaml")"
expect "prefix: policy names" "$(names "${RENDERED}")" '["gs-verify-image-signatures-gsoci-circleci-keyless","gs-verify-image-signatures-my-corp"]'
ok "policyNamePrefix gs-: policy name gs-verify-image-signatures-my-corp"

# 7. name must equal the giantswarm key ------------------------------------------
cat >"${tmp}/name-mismatch.yaml" <<'YAML'
imageVerification:
  giantswarm:
    gsoci-circleci-keyless:
      name: other
YAML
if out="$(helm template kp "${chart}" -f "${tmp}/name-mismatch.yaml" 2>&1)"; then
  fail "name mismatch: helm template succeeded, expected a failure"
fi
case "${out}" in
  *'name "other" must equal its key "gsoci-circleci-keyless"'*) ;;
  *) fail "name mismatch: helm template failed without the key/name message: ${out}" ;;
esac
ok "giantswarm name differing from its key: helm template fails with the key/name message"

# 8. Generated schema -------------------------------------------------------------
ref_path='#/properties/imageVerification/properties/giantswarm/properties/gsoci-circleci-keyless'
# shellcheck disable=SC2016 # "$ref" is a yq key, not a shell expansion
expect "schema: customer.items.\$ref" \
  "$(yq -o=json -I=0 '.properties.imageVerification.properties.customer.items["$ref"]' "${schema}")" \
  "\"${ref_path}\""
expect "schema: referenced subschema requires name, images, attestors" \
  "$(yq -o=json -I=0 '.properties.imageVerification.properties.giantswarm.properties.gsoci-circleci-keyless.required | contains(["name", "images", "attestors"])' "${schema}")" \
  'true'
ok "schema: customer.items refs the giantswarm subschema, which requires name, images, attestors"

# 9. Glob characters ----------------------------------------------------------------
cat >"${tmp}/bad-glob.yaml" <<YAML
imageVerification:
  customer:
    - name: badglob
      images: ["registry.example/{a,b}/app"]
      attestors:
        - name: ci
          key:
            publicKey: |
${indented_key}
YAML
if out="$(helm template kp "${chart}" --skip-schema-validation -f "${tmp}/bad-glob.yaml" 2>&1)"; then
  fail "bad glob: helm template succeeded, expected a failure"
fi
case "${out}" in
  *'only * is supported as a wildcard'*) ;;
  *) fail "bad glob: helm template failed without the wildcard message: ${out}" ;;
esac
ok "glob with {a,b}: helm template fails with 'only * is supported as a wildcard'"

# 10. Policy name length --------------------------------------------------------------
long_name="acme-production-registry-verifier-eu-west"
cat >"${tmp}/long-name.yaml" <<YAML
policyNamePrefix: gs-
imageVerification:
  customer:
    - name: ${long_name}
      images: ["registry.example/acme/*"]
      attestors:
        - name: ci
          key:
            publicKey: |
${indented_key}
YAML
if out="$(helm template kp "${chart}" -f "${tmp}/long-name.yaml" 2>&1)"; then
  fail "long name: helm template succeeded, expected a failure"
fi
case "${out}" in
  *"is 68 characters long, the limit is 63"*) ;;
  *) fail "long name: helm template failed without the length message: ${out}" ;;
esac
ok "policy name gs-verify-image-signatures-${long_name}: helm template fails with 'is 68 characters long, the limit is 63'"

# 11. Attestor name starting with a digit -------------------------------------------------
cat >"${tmp}/digit-attestor.yaml" <<YAML
imageVerification:
  customer:
    - name: digit
      images: ["registry.example/digit/*"]
      attestors:
        - name: 1ci
          key:
            publicKey: |
${indented_key}
YAML
if out="$(helm template kp "${chart}" --skip-schema-validation -f "${tmp}/digit-attestor.yaml" 2>&1)"; then
  fail "digit attestor: helm template succeeded, expected a failure"
fi
case "${out}" in
  *'name "1ci" must match ^[a-z][a-z0-9]*$'*) ;;
  *) fail "digit attestor: helm template failed without the attestor name message: ${out}" ;;
esac
ok "attestor name 1ci: helm template fails with the CEL identifier message"

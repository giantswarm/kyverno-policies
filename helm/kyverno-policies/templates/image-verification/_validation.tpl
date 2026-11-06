{{/* imageVerification.validate fails the render on verifier mistakes the values schema cannot catch. */}}
{{- define "imageVerification.validate" -}}
{{- $iv := .Values.imageVerification -}}
{{- $allowedProviders := list "default" "azure" "google" "amazon" "github" -}}
{{- $celReserved := list "in" "as" "null" "true" "false" "break" "const" "continue" "else" "for" "function" "if" "import" "let" "loop" "package" "namespace" "return" "var" "void" "while" -}}
{{- $verifiers := list -}}
{{- range $key := keys ($iv.giantswarm | default dict) | sortAlpha -}}
  {{- $v := get $iv.giantswarm $key -}}
  {{- if not $v.name -}}
    {{- fail (printf "imageVerification.giantswarm.%s: name is required and must equal its key." $key) -}}
  {{- end -}}
  {{- if ne (toString $v.name) $key -}}
    {{- fail (printf "imageVerification.giantswarm.%s: name %q must equal its key %q." $key (toString $v.name) $key) -}}
  {{- end -}}
  {{- $verifiers = append $verifiers (dict "path" (printf "imageVerification.giantswarm.%s" $key) "verifier" $v) -}}
{{- end -}}
{{- range $i, $v := $iv.customer | default list -}}
  {{- $verifiers = append $verifiers (dict "path" (printf "imageVerification.customer[%d]" $i) "verifier" $v) -}}
{{- end -}}
{{- $names := dict -}}
{{- range $verifiers -}}
  {{- $path := .path -}}
  {{- $v := .verifier -}}
  {{- if not $v.name -}}
    {{- fail (printf "%s: name is required." $path) -}}
  {{- end -}}
  {{- if hasKey $names $v.name -}}
    {{- fail (printf "%s: name %q is already used by %s; verifier names must be unique across imageVerification.giantswarm and imageVerification.customer." $path $v.name (get $names $v.name)) -}}
  {{- end -}}
  {{- $_ := set $names $v.name $path -}}
  {{- if not (regexMatch "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$" (toString $v.name)) -}}
    {{- fail (printf "%s: name %q must match ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$." $path (toString $v.name)) -}}
  {{- end -}}
  {{- $policyName := printf "%sverify-image-signatures-%s" $.Values.policyNamePrefix $v.name -}}
  {{- if gt (len $policyName) 63 -}}
    {{- fail (printf "%s: policy name %q is %d characters long, the limit is 63 (Kyverno uses it in the report label ivpol.kyverno.io/<name>); shorten the name or policyNamePrefix." $path $policyName (len $policyName)) -}}
  {{- end -}}
  {{- if not $v.images -}}
    {{- fail (printf "%s: images must list at least one image glob." $path) -}}
  {{- end -}}
  {{- range $field := list "images" "excludeImages" -}}
    {{- range $j, $glob := get $v $field | default list -}}
      {{- if not (regexMatch "^[A-Za-z0-9._/:@*-]+$" (toString $glob)) -}}
        {{- fail (printf "%s.%s[%d]: glob %q may contain only letters, digits and . _ / : @ - *; only * is supported as a wildcard." $path $field $j (toString $glob)) -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
  {{- $attestors := $v.attestors | default list -}}
  {{- if not $attestors -}}
    {{- fail (printf "%s: attestors must list at least one attestor." $path) -}}
  {{- end -}}
  {{- if hasKey $v "minVerifiedAttestors" -}}
    {{- $min := int $v.minVerifiedAttestors -}}
    {{- if lt $min 1 -}}
      {{- fail (printf "%s: minVerifiedAttestors must be at least 1, got %d." $path $min) -}}
    {{- end -}}
    {{- if gt $min (len $attestors) -}}
      {{- fail (printf "%s: minVerifiedAttestors (%d) exceeds the number of attestors (%d)." $path $min (len $attestors)) -}}
    {{- end -}}
  {{- end -}}
  {{- $attestorNames := dict -}}
  {{- range $j, $a := $attestors -}}
    {{- $apath := printf "%s.attestors[%d]" $path $j -}}
    {{- if not (regexMatch "^[a-z][a-z0-9]*$" (toString $a.name)) -}}
      {{- fail (printf "%s: name %q must match ^[a-z][a-z0-9]*$ because it becomes a CEL identifier." $apath (toString $a.name)) -}}
    {{- end -}}
    {{- if has (toString $a.name) $celReserved -}}
      {{- fail (printf "%s: name %q is a CEL reserved word and cannot be used as an attestor name." $apath (toString $a.name)) -}}
    {{- end -}}
    {{- if hasKey $attestorNames $a.name -}}
      {{- fail (printf "%s: attestor name %q is used twice in this verifier." $apath $a.name) -}}
    {{- end -}}
    {{- $_ := set $attestorNames $a.name true -}}
    {{- if and $a.keyless $a.key -}}
      {{- fail (printf "%s: set exactly one of keyless or key, not both." $apath) -}}
    {{- end -}}
    {{- if not (or $a.keyless $a.key) -}}
      {{- fail (printf "%s: set exactly one of keyless or key." $apath) -}}
    {{- end -}}
    {{- if $a.keyless -}}
      {{- if not $a.keyless.issuer -}}
        {{- fail (printf "%s.keyless: issuer is required." $apath) -}}
      {{- end -}}
      {{- if eq (empty $a.keyless.subject) (empty $a.keyless.subjectRegExp) -}}
        {{- fail (printf "%s.keyless: set exactly one of subject or subjectRegExp." $apath) -}}
      {{- end -}}
    {{- end -}}
    {{- if and $a.key (not $a.key.publicKey) -}}
      {{- fail (printf "%s.key: publicKey is required." $apath) -}}
    {{- end -}}
  {{- end -}}
  {{- $credentials := $v.credentials | default dict -}}
  {{- range $credentials.providers | default list -}}
    {{- if not (has . $allowedProviders) -}}
      {{- fail (printf "%s.credentials: provider %q is not one of %s." $path (toString .) (join ", " $allowedProviders)) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- end -}}

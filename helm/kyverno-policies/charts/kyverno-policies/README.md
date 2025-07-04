# kyverno-policies

Kubernetes Pod Security Standards implemented as Kyverno policies

![Version: 3.4.2](https://img.shields.io/badge/Version-3.4.2-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: v1.14.2](https://img.shields.io/badge/AppVersion-v1.14.2-informational?style=flat-square)

## About

This chart contains Kyverno's implementation of the Kubernetes Pod Security Standards (PSS) as documented at https://kubernetes.io/docs/concepts/security/pod-security-standards/ and are a Helm packaged version of those found at https://github.com/kyverno/policies/tree/main/pod-security. The goal of the PSS controls is to provide a good starting point for general Kubernetes cluster operational security. These controls are broken down into two categories, Baseline and Restricted. Baseline policies implement the most basic of Pod security controls while Restricted implements more strict controls. Restricted is cumulative and encompasses those listed in Baseline.

The following policies are included in each profile.

**Baseline**

* disallow-capabilities
* disallow-host-namespaces
* disallow-host-path
* disallow-host-ports
* disallow-host-process
* disallow-privileged-containers
* disallow-proc-mount
* disallow-selinux
* restrict-apparmor-profiles
* restrict-seccomp
* restrict-sysctls

**Restricted**

* disallow-capabilities-strict
* disallow-privilege-escalation
* require-run-as-non-root-user
* require-run-as-nonroot
* restrict-seccomp-strict
* restrict-volume-types

An additional policy "require-non-root-groups" is included in an `other` group as this was previously included in the official PSS controls but since removed.

For the latest version of these PSS policies, always refer to the kyverno/policies repo at https://github.com/kyverno/policies/tree/main/pod-security.

## Deploy custom policies
If you have custom policies you would like to deploy as part of the Helm release, provide their manifests in `.Values.customPolicies`:
````yaml
customPolicies:
  - apiVersion: kyverno.io/v1
    kind: ClusterPolicy
    metadata: # metadata
    spec: # spec
````

## Installing the Chart

These PSS policies presently have a minimum requirement of Kyverno 1.6.0.

```console
## Add the Kyverno Helm repository
$ helm repo add kyverno https://kyverno.github.io/kyverno/

## Install the Kyverno Policies Helm chart
$ helm install kyverno-policies --namespace kyverno kyverno/kyverno-policies
```

## Uninstalling the Chart

To uninstall/delete the `kyverno-policies` chart:

```console
$ helm delete -n kyverno kyverno-policies
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| policyKind | string | `"ClusterPolicy"` | Policy kind (`ClusterPolicy`, `Policy`) Set to `Policy` if you need namespaced policies and not cluster policies |
| podSecurityStandard | string | `"baseline"` | Pod Security Standard profile (`baseline`, `restricted`, `privileged`, `custom`). For more info https://kyverno.io/policies/pod-security. |
| podSecuritySeverity | string | `"medium"` | Pod Security Standard (`low`, `medium`, `high`). |
| podSecurityPolicies | list | `[]` | Policies to include when `podSecurityStandard` is `custom`. |
| includeOtherPolicies | list | `[]` | Additional policies to include from `other`. |
| includeRestrictedPolicies | list | `[]` | Additional policies to include from `restricted`. |
| customPolicies | list | `[]` | Additional custom policies to include. |
| failurePolicy | string | `"Fail"` | API server behavior if the webhook fails to respond ('Ignore', 'Fail') For more info: https://kyverno.io/docs/writing-policies/policy-settings/ |
| validationFailureAction | string | `"Audit"` | Validation failure action (`Audit`, `Enforce`). For more info https://kyverno.io/docs/writing-policies/validate. |
| validationFailureActionByPolicy | object | `{}` | Define validationFailureActionByPolicy for specific policies. Override the defined `validationFailureAction` with a individual validationFailureAction for individual Policies. |
| validationFailureActionOverrides | object | `{"all":[]}` | Define validationFailureActionOverrides for specific policies. The overrides for `all` will apply to all policies. |
| validationAllowExistingViolations | bool | `true` | Validate already existing resources. For more info https://kyverno.io/docs/policy-types/. |
| policyExclude | object | `{}` | Exclude resources from individual policies. Policies with multiple rules can have individual rules excluded by using the name of the rule as the key in the `policyExclude` map. |
| policyPreconditions | object | `{}` | Add preconditions to individual policies. Policies with multiple rules can have individual rules excluded by using the name of the rule as the key in the `policyPreconditions` map. |
| autogenControllers | string | `""` | Customize the target Pod controllers for the auto-generated rules. (Eg. `none`, `Deployment`, `DaemonSet,Deployment,StatefulSet`) For more info https://kyverno.io/docs/writing-policies/autogen/. |
| nameOverride | string | `nil` | Name override. |
| customAnnotations | object | `{}` | Additional Annotations. |
| customLabels | object | `{}` | Additional labels. |
| background | bool | `true` | Policies background mode |
| skipBackgroundRequests | bool | `nil` | SkipBackgroundRequests bypasses admission requests that are sent by the background controller |
| kyvernoVersion | string | `"autodetect"` | Kyverno version The default of "autodetect" will try to determine the currently installed version from the deployment |
| kubeVersionOverride | string | `nil` | Kubernetes version override Override default value of kubeVersion set by release team taken from Chart.yaml with custom value. Ideally range of versions no more than two prior (ex., 1.28-1.31), must be enclosed in quotes. |

## Source Code

* <https://github.com/kyverno/policies>

## Requirements

Kubernetes: `>=1.25.0-0`

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| kyverno-maintainers | <cncf-kyverno-maintainers@lists.cncf.io> |  |

## Changes

### v2.3.4

* Do not evaluate `foreach` policies on DELETE

### v2.3.3

* Add policyPreconditions value to allow policies and rules to have preconditions added

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)

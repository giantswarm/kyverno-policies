# kyverno-policies

Kubernetes Pod Security Standards implemented as Kyverno policies

**Homepage:** <https://github.com/giantswarm/kyverno-policies>

## Source Code

* <https://github.com/giantswarm/kyverno-policies>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | kyverno-policies | 3.9.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| kyverno-policies.policyType | string | `"ValidatingPolicy"` |  |
| kyverno-policies.podSecurityStandard | string | `"restricted"` |  |
| kyverno-policies.customLabels."application.giantswarm.io/team" | string | `"shield"` |  |
| policyNamePrefix | string | `""` |  |
| bestPracticesPolicies.policies.check-resources-request-and-limits-ratio.enabled | bool | `false` |  |
| bestPracticesPolicies.policies.check-resources-request-and-limits-ratio.mode | string | `"Audit"` |  |
| bestPracticesPolicies.policies.disallow-latest-tag.enabled | bool | `true` |  |
| bestPracticesPolicies.policies.disallow-latest-tag.mode | string | `"Audit"` |  |
| bestPracticesPolicies.policies.prevent-bare-pods.enabled | bool | `true` |  |
| bestPracticesPolicies.policies.prevent-bare-pods.mode | string | `"Audit"` |  |
| bestPracticesPolicies.policies.require-container-requests-and-limits.enabled | bool | `false` |  |
| bestPracticesPolicies.policies.require-container-requests-and-limits.mode | string | `"Audit"` |  |
| bestPracticesPolicies.policies.require-emptydir-requests-and-limits.enabled | bool | `true` |  |
| bestPracticesPolicies.policies.require-emptydir-requests-and-limits.mode | string | `"Audit"` |  |
| bestPracticesPolicies.policies.require-pod-probes.enabled | bool | `false` |  |
| bestPracticesPolicies.policies.require-pod-probes.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.audit-event-on-exec.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.add-default-deny-network-policy.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.add-default-deny-network-policy.deleteNetworkPolicyOnKyvernoPolicyDeletion | bool | `false` |  |
| supplementalSecurityPolicies.policies.add-default-deny-network-policy.generateForExistingNamespaces | bool | `false` |  |
| supplementalSecurityPolicies.policies.add-default-deny-network-policy.networkPolicy.policyName | string | `"default-deny"` |  |
| supplementalSecurityPolicies.policies.add-default-deny-network-policy.networkPolicy.blockIngress | bool | `true` |  |
| supplementalSecurityPolicies.policies.add-default-deny-network-policy.networkPolicy.blockEgress | bool | `true` |  |
| supplementalSecurityPolicies.policies.check-serviceaccount-secrets.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.check-serviceaccount-secrets.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.disallow-gitrepo-volume.enabled | bool | `true` |  |
| supplementalSecurityPolicies.policies.disallow-gitrepo-volume.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.require-ro-rootfs.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.require-ro-rootfs.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.restrict-binding-clusteradmin.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.restrict-binding-clusteradmin.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.restrict-binding-system-groups.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.restrict-binding-system-groups.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.restrict-external-ips.enabled | bool | `true` |  |
| supplementalSecurityPolicies.policies.restrict-external-ips.mode | string | `"Audit"` |  |
| supplementalSecurityPolicies.policies.restrict-sa-automount-sa-token.enabled | bool | `false` |  |
| supplementalSecurityPolicies.policies.restrict-sa-automount-sa-token.mode | string | `"Audit"` |  |
| debugAccessPolicies.allowedDebugContainerImages | list | `[]` |  |
| debugAccessPolicies.authorizedDebugTargets[0].namespaces | list | `[]` |  |
| debugAccessPolicies.authorizedDebugTargets[0].allDeployments | bool | `false` |  |
| debugAccessPolicies.authorizedDebugTargets[0].deployments | list | `[]` |  |
| debugAccessPolicies.authorizedDebugTargets[0].allowedDebugContainerImages | list | `[]` |  |
| debugAccessPolicies.policies.disallow-ephemeral-containers.enabled | bool | `false` |  |
| debugAccessPolicies.policies.disallow-ephemeral-containers.mode | string | `"Audit"` |  |
| debugAccessPolicies.policies.disallow-unapproved-debug-access.enabled | bool | `false` |  |
| debugAccessPolicies.policies.disallow-unapproved-debug-access.mode | string | `"Audit"` |  |
| debugAccessPolicies.policies.block-expired-exceptions.enabled | bool | `false` |  |
| debugAccessPolicies.policies.block-expired-exceptions.mode | string | `"Audit"` |  |
| debugAccessPolicies.policies.purge-expired-exceptions.enabled | bool | `false` |  |
| debugAccessPolicies.policies.purge-expired-exceptions.mode | string | `"Audit"` |  |
| debugAccessPolicies.policies.purge-expired-exceptions.cleanupSchedule | string | `"*/27 * * * *"` |  |
| debugAccessPolicies.policies.purge-expired-exceptions.targetAnnotation | string | `"policy.giantswarm.io/exception-expires-at"` |  |

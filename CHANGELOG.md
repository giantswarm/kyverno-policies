# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add supplemental policies `restrict-external-ips`, `require-ro-rootfs`, and enable upstream policy `require-non-root-groups`.
- Add supplemental policy to generate default deny-all Network Policies in newly created namespaces.

## [0.21.1] - 2024-12-11

### Changed

- Add `application.giantswarm.io/team` label to policies.

## [0.21.0] - 2024-09-25

### Changed

- Update to upstream `Kyverno Policies` version 1.12.5.
- Don't push to vsphere-app-collection, capz-app-collection, capa-app-collection or cloud-director-app-collection. We started to consume kyverno-policies from security-bundle.

## [0.20.2] - 2023-12-06

### Fixed

- Fix team ownership

## [0.20.1] - 2023-09-21

### Changed

- Update to upstream `Kyverno Policies` version 1.10.3.

## [0.20.0] - 2023-06-23

### Changed

- Update to upstream `Kyverno Policies` version 1.10.0.
- Update CI to use newer `ats` and the `abs` executor.

## [0.19.0] - 2023-05-31

### Changed

- Enable PSS Restricted policies by default.

### Removed

- Stop pushing to `openstack-app-collection`.

## [0.18.1] - 2023-02-15

### Added

- Push to `cloud-director` app collection.
- Push to `capz` app collection.

## [0.18.0] - 2022-11-16

### Changed

- Update to upstream v1.7.5 policies.

## [0.17.2] - 2022-08-05

## [0.17.1] - 2022-04-06

### Added

- Push policies to `giantswarm` catalog.

## [0.17.0] - 2022-04-05

### Changed

- Track upstream PSS policies with a subtree.
- Push PSS policies to AWS, Azure, KVM, OpenStack, and VSphere catalogs and collections.
- Remove catalog and collections push for common and shared policies.

## [0.16.0] - 2022-03-02

### Changed

- Policies no longer the `cluster-apps-operator.giantswarm.io/version` label since `cluster-apps-operator` don't use it.

## [0.15.0] - 2022-02-28

### Changed

- Add default audit log config file to `KubeadmControlPlane`.

## [0.14.0] - 2022-01-19

### Added

- Support all API versions for CAPI resources

### Changed

- Default Azure subscription ID by getting value directly from organization credentials secret.

## [0.13.2] - 2022-01-13

### Fixed

- Fixed `block-bulk-certconfigs-delete` policy

## [0.13.1] - 2022-01-13

### Added

- Add `block-bulk-certconfigs-delete` policy

## [0.13.0] - 2022-01-05

### Added

- Add `policies-openstack` for OpenStack-specific policies.
- Add policy for OpenStack which defaults `failureDomain` based on `MachineDeployment`
  request's `machine-deployment.giantswarm.io/failure-domain` label.

## [0.12.0] - 2021-12-09

### Added

- Add `cluster-apps-operator.giantswarm.io/watching` label to Cluster CRs so they will
  be watched by `cluster-apps-operator` >=v1.1.0 (deployed by an app collection) in addition
  to <v1.1.0 (deployed by release-operator).

## [0.11.0] - 2021-11-30

### Added

- Tilt support.

### Changed

- The api-server `extraVolumes` are appended instead of over writing the existing ones.

## [0.10.0] - 2021-11-19

### Changed

- Apply policies to v20 even when v20 contains suffixes in its name.

### Added

- Policy to apply `audit-policy.yaml` to kubeadmconfig

## [0.9.2] - 2021-10-26

### Changed

- Remove `PodSecurityPolicy` from the enabled api-server admission plugins.

## [0.9.1] - 2021-10-20

### Fixed

- Removed `encryption-provider-config` and `audit-policy-file` flags until we can confirm the file exists on the machine images

## [0.9.0] - 2021-10-19

### Added

- CircleCI job to validate policies

### Changed

- Updated kubelet and api server flags to handle duplicates

## [0.8.0] - 2021-10-13

### Added

- kubelet and api server flags for CAPI clusters.

## [0.7.1] - 2021-10-12

### Fixed

- Fix annotation name in subscription id defaulting rule.

## [0.7.0] - 2021-10-12

### Added

- Default SubscriptionID field for `AzureCluster` CRs.

### Changed

- Add test setup for `vsphere` policies.

## [0.6.2] - 2021-10-11

### Added

- Set kubelet extra argument `node-ip` for worker and masters.
- Validate deprecated APIs.

## [0.6.1] - 2021-10-06

## [0.6.0] - 2021-10-06

### Changed

- Use `ats` for integration testing instead of `abs`.
- Rename `vmware` chart and policies to `vsphere`.

## [0.6.0] - 2021-10-05

### Added

- Add CRDs related to kubeadm controlplane to CI.
- Add policies to configure default disk sizes and disk initialization for CAPA cluster.

### Changed

- Keep existing `node-labels` when ensuring the `role=worker` label exists in `KubeadmConfig`s.

## [0.5.0] - 2021-09-13

### Added

- Add AWS CNI security group rules to `AWSCluster` CR.

## [0.4.0] - 2021-09-03

### Added

- Default `spec.location` field for CAPZ `AzureMachinePool` CRs.

## [0.3.0] - 2021-09-02

### Added

- Default `spec.location` field for CAPZ `AzureCluster` CRs.

## [0.2.0] - 2021-08-31

### Changed

- Ensure `controllerManager`'s extra arg `allocate-node-cidrs` is set to true in `KubeadmControlPlane` for Azure clusters.

## [0.1.3] - 2021-08-27

### Changed

- Ensure that `kubeadm` configs are not defaulted for control planes.

## [0.1.2] - 2021-08-25

### Removed

- Remove Service Monitor policy pending upstream bug fix.

## [0.1.1] - 2021-08-25

### Fixed

- Fix group `controlplane` for `AWSManagedControlPlane`CR.

## [0.1.0] - 2021-08-25

### Added

- Defaulting `region` and `sshKeyName` in AWSManagedControlPlane CR.

## [0.0.11] - 2021-08-23

### Changed

- Enable labeling policies to work with v1alpha4 types.

## [0.0.10] - 2021-08-18

### Fixed

- Ensure the Silence Cluster policy do not replace matchers.

## [0.0.9] - 2021-08-17

### Fixed

- Fix CI issues for `policies-shared`.

## [0.0.8] - 2021-08-17

### Added

- Add Service Monitor policy to configure the default labelling schema.

## [0.0.7] - 2021-08-11

### Added

- Add documentation to test cases.
- Add policy to not silence heartbeats

### Changed

- Restructured test fixtures.

## [0.0.6] - 2021-07-16

## [0.0.5] - 2021-07-16

### Added

- Add default for cluster description.
- Add defaulting to set custom labels on worker nodes.

## [0.0.4] - 2021-07-14

## [0.0.3] - 2021-07-13

### Added

- Add default for aws control plane instance type.

## [0.0.2] - 2021-07-12

### Added

- Add defaulting for `aws` values.
- Add integration tests for `aws`.

### Changed

- Reduced number of policy files.
- Restructured CI setup to use Makefile.

## [0.0.1] - 2021-06-02

[Unreleased]: https://github.com/giantswarm/kyverno-policies/compare/v0.21.1...HEAD
[0.21.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.21.0...v0.21.1
[0.21.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.20.2...v0.21.0
[0.20.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.20.1...v0.20.2
[0.20.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.20.0...v0.20.1
[0.20.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.19.0...v0.20.0
[0.19.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.18.1...v0.19.0
[0.18.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.18.0...v0.18.1
[0.18.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.17.2...v0.18.0
[0.17.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.17.1...v0.17.2
[0.17.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.17.0...v0.17.1
[0.17.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.13.2...v0.14.0
[0.13.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.13.1...v0.13.2
[0.13.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.9.2...v0.10.0
[0.9.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.6.2...v0.7.0
[0.6.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.6.0...v0.6.0
[0.6.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/giantswarm/kyverno-policies/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/giantswarm/kyverno-policies/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.11...v0.1.0
[0.0.11]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.9...v0.0.8
[0.0.7]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/giantswarm/kyverno-policies/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/giantswarm/kyverno-policies/releases/tag/v0.0.1

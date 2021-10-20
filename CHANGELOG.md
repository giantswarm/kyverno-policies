# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/giantswarm/kyverno-policies/compare/v0.9.1...HEAD
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

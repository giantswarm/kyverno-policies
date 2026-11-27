# kyverno-policies

This repository tracks the [upstream Kyverno PSS policies](https://github.com/kyverno/kyverno/tree/main/charts/kyverno-policies) and is used for deploying PSS policies alongside our [kyverno-app](https://github.com/giantswarm/kyverno-app).

## Repository structure

We implement an app according to the [general Giant Swarm app platform](https://docs.giantswarm.io/overview/fleet-management/app-management/) which relies on Helm for application management.

The `policies` folder contains the policies which are then escaped to be compliant with helm specific syntax.
We use `[[` and  `]]` delimeters to handle cases where variables should be managed by helm.

The `hack` folder contains scripts which are used during local development and in CI.
These scripts enable us to easily set up a local testing environment.

## Image verification

The chart renders one `ImageValidatingPolicy` (Kyverno 1.18 or newer) per verifier configured under `imageVerification` in [`values.yaml`](helm/kyverno-policies/values.yaml). Giant Swarm's verifier `gsoci-circleci-keyless` audits `gsoci.azurecr.io/giantswarm/*` by default; customers add their own under `imageVerification.customer`.

`make helm-test` runs the helm-unittest suite in [`helm/kyverno-policies/tests`](helm/kyverno-policies/tests), which asserts the rendered policies for several value sets. The Chainsaw test in [`tests/chainsaw/verify-image-signatures`](tests/chainsaw/verify-image-signatures) needs outbound HTTPS from the kind node and `make kyverno-fast-background-scan` after `make install-kyverno`.

## Development

### Prerequisites

1. `make` installed
2. `kubectl` installed
3. `kind` installed
4. `helm` installed
5. `chainsaw` installed ([Chainsaw installation guide](https://kyverno.github.io/chainsaw/latest/quick-start/install/))

### Generate policies

To generate the policies in the `helm` folder structure:
```bash
make generate
```

## Policy types

Every Giant Swarm policy in this chart exists both as a legacy `kyverno.io` policy and as a CEL policy (`policies.kyverno.io/v1`, tested with Kyverno 1.19.2). The legacy types are the default.

- The validating policies follow `kyverno-policies.policyType`, the same switch that selects the upstream Pod Security Standards policies: `ClusterPolicy` (default) or `ValidatingPolicy`.
- The generating and cleanup policies have their own `policyType`: `audit-event-on-exec` and `add-default-deny-network-policy` take `ClusterPolicy` or `GeneratingPolicy`, and `purge-expired-exceptions` takes `ClusterCleanupPolicy` or `DeletingPolicy`.
- `mode: Audit|Enforce` works for both types. A ValidatingPolicy gets `validationActions: [Audit]` or `[Deny]`.

Before switching, note:

- `kyverno.io` PolicyExceptions only apply to ClusterPolicies. A CEL policy needs a `policies.kyverno.io/v1` PolicyException with `policyRefs: [{name: <policy>, kind: ValidatingPolicy}]`.
- Switching `add-default-deny-network-policy` replaces one policy with the other. On Kyverno 1.19.2 with the default values, switching from ClusterPolicy to GeneratingPolicy kept the NetworkPolicies already generated, but switching back deleted them. Set `generateForExistingNamespaces: true` to have the new policy recreate them.
- A GeneratingPolicy always registers its webhook with `failurePolicy: Ignore`, so while Kyverno is down namespaces and execs go through without the generated object.
- A ValidatingPolicy that matches `pods` is not evaluated at admission for `kubectl debug` (`pods/ephemeralcontainers`), only by the background scan. This includes the upstream Pod Security Standards policies: on Kyverno 1.19.2 a debug container without a `securityContext` is denied in ClusterPolicy mode and admitted in ValidatingPolicy mode. `disallow-ephemeral-containers` and `disallow-unapproved-debug-access` match the subresource explicitly, so they still apply.
- Autogen for Pod controllers in CEL policies does not cover ReplicationControllers.

## Testing

Tests are implemented using [Chainsaw](https://kyverno.github.io/chainsaw/), a declarative testing framework for Kubernetes.

### Test structure

Tests are located in `tests/chainsaw/` with the following structure:

```
tests/chainsaw/
├── _steps-templates/           # Reusable test step templates
│   └── policy-ready.yaml       # Waits for a policy of either type to be ready
├── check-policy-ready/         # Test that verifies all policies are ready
│   └── chainsaw-test.yaml
├── values.yaml                 # Helm values for test configuration (legacy policy types, used by CI)
├── values-cel.yaml             # Overlay that switches every policy to its CEL type
└── <policy-name>/              # Individual policy tests
    ├── chainsaw-test.yaml      # Test definition
    ├── good-pod.yaml           # Resource that should be allowed
    └── bad-pod.yaml            # Resource that should be blocked
```

### Running tests

1. Create a Kind cluster and install Kyverno:
```bash
make kind-create
make install-kyverno
```

2. Install the policies with test configuration:
```bash
make install-policies
```

3. Run all Chainsaw tests:
```bash
chainsaw test --test-dir tests/chainsaw/
```

Tests are type-agnostic. To run them against the CEL policies, install with the overlay as well. CI runs the legacy types only. In CEL mode `restrict-apparmor-profiles` fails, because the vendored upstream CEL policy compares `localhost/*` literally:
```bash
helm upgrade --install kyverno-policies helm/kyverno-policies \
  --values tests/chainsaw/values.yaml --values tests/chainsaw/values-cel.yaml
```

To run a specific test:
```bash
chainsaw test --test-dir tests/chainsaw/disallow-capabilities/
```

### Writing tests

Each policy test follows a simple pattern:

1. Create a directory under `tests/chainsaw/<policy-name>/`
2. Add a `chainsaw-test.yaml` that defines the test steps
3. Add resource files for both allowed and blocked scenarios

Example test (`chainsaw-test.yaml`):
```yaml
apiVersion: chainsaw.kyverno.io/v1alpha1
kind: Test
metadata:
  name: disallow-privileged-containers
spec:
  steps:
  - name: create a bad pod
    try:
    - create:
        expect:
        - check:
            ($error != null): true
        file: bad-pod.yaml
  - name: create a good pod
    try:
    - create:
        expect:
        - check:
            ($error != null): false
        file: good-pod.yaml
```

The test uses `create` to attempt resource creation and checks:
- `($error != null): true` - expects the policy to **block** the resource
- `($error != null): false` - expects the policy to **allow** the resource

### Test configuration

The `tests/chainsaw/values.yaml` file configures policies for testing. Policies should be set to `Enforce` mode to verify blocking behavior. A policy that would deny other tests' resources in `Enforce` (for example `require-pod-probes` or `prevent-bare-pods`) runs in `Audit`, and its test asserts the `PolicyReport` result instead:

```yaml
kyverno-policies:
  validationFailureAction: Enforce
```

### Tilt
You can use Tilt for fast feedback loops.

First create the local `kind` cluster
```shell
make kind-create
```

Then you just need to start `tilt`
```shell
make tilt-up
```

# kyverno-policies

This repository tracks the [upstream Kyverno PSS policies](https://github.com/kyverno/kyverno/tree/main/charts/kyverno-policies) and is used for deploying PSS policies alongside our [kyverno-app](https://github.com/giantswarm/kyverno-app).

## Repository structure

We implement an app according to the [general Giant Swarm app platform](https://docs.giantswarm.io/app-platform/) which relies on Helm for application management.

The `policies` folder contains the policies which are then escaped to be compliant with helm specific syntax.
We use `[[` and  `]]` delimeters to handle cases where variables should be managed by helm.

The `hack` folder contains scripts which are used during local development and in CI.
These scripts enable us to easily set up a local testing environment.

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

## Testing

Tests are implemented using [Chainsaw](https://kyverno.github.io/chainsaw/), a declarative testing framework for Kubernetes.

### Test structure

Tests are located in `tests/chainsaw/` with the following structure:

```
tests/chainsaw/
├── _steps-templates/           # Reusable test step templates
│   └── cluster-policy-ready.yaml
├── check-policy-ready/         # Test that verifies all policies are ready
│   └── chainsaw-test.yaml
├── values.yaml                 # Helm values for test configuration
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

The `tests/chainsaw/values.yaml` file configures policies for testing. Policies should be set to `Enforce` mode to verify blocking behavior:

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

# kyverno-policies

This repository contains kyverno policies which Giant Swarm uses.

## Repository structure

We implement an app according to the [general Giant Swarm app platform](https://docs.giantswarm.io/app-platform/) which relies on Helm for application management.

The `policies` folder contains the policies which are then escaped to be compliant with helm specific syntax.
We use `[[` and  `]]` delimeters to handle cases where variables should be managed by helm.

The `hack` folder contains scripts which are used during local development and in CI.
These scripts enable us to easily set up a local testing environment.

## Development

There are only very few prerequists for local testing:
1. `make` has to be installed
2. `kubectl` has to be installed
3. `kind` has to be installed
4. [dabs.sh](https://raw.githubusercontent.com/giantswarm/app-build-suite/v0.2.3/dabs.sh) has to be accessible.

Tests are implemented with [pytest](https://docs.pytest.org) and the framework is supplied by [app-build-suite](https://github.com/giantswarm/app-build-suite/blob/master/docs/tutorial.md).

Executing the integration tests can be done with this simple set of commands:
```bash
make setup # Creates the kind cluster and installs all dependencies.
./dabs.sh -c ./helm/policies-aws # Executes the tests related to the AWS policies against the kind cluster.
```

To only generate the policies in the `helm` folder structure:
```bash
make generate
```

import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_cluster_policy(kubernetes_cluster) -> None:
    cluster_name = "test-cluster"
    release_version = "20.0.0-v1alpha3"
    capi_core_version = "0.0.2"
    cluster_operator_version = "2.0.0"

    obj = {}

    ensure.release(kubernetes_cluster.kubectl, release_version,
                   cluster_operator_version, capi_core_version)
    ensure.cluster(kubernetes_cluster.kubectl,
                   cluster_name, release_version)

    raw = kubernetes_cluster.kubectl(
        f"get cluster {cluster_name}", output="yaml")

    cluster = yaml.safe_load(raw)

    assert cluster['metadata']['labels']['cluster-operator.giantswarm.io/version'] == cluster_operator_version
    assert cluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == capi_core_version


@pytest.mark.smoke
def test_machine_deployment_policy(kubernetes_cluster) -> None:
    machine_deployment_name = "test-md"
    cluster_name = "test-cluster-md"
    release_version = "20.0.0-v1alpha4"
    capi_core_version = "0.0.2"
    cluster_operator_version = "2.0.0"

    obj = {}

    ensure.release(kubernetes_cluster.kubectl, release_version,
                   cluster_operator_version, capi_core_version)
    ensure.cluster(kubernetes_cluster.kubectl,
                   cluster_name, release_version)
    ensure.machine_deployment(kubernetes_cluster.kubectl, cluster_name,
                              machine_deployment_name)

    raw = kubernetes_cluster.kubectl(
        f"get MachineDeployment {machine_deployment_name}", output="yaml")

    md = yaml.safe_load(raw)

    assert md['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == capi_core_version

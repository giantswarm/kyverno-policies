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
def test_aws_cluster_policy(kubernetes_cluster) -> None:
    cluster_name = "test-cluster-1"
    release_version = "20.0.0"
    capa_version = "capi"
    cluster_apps_operator_version = "2.0.0"

    ensure.release(kubernetes_cluster.kubectl, release_version,
                   cluster_apps_operator_version)
    ensure.cluster(kubernetes_cluster.kubectl,
                   cluster_name, release_version)
    ensure.emptyawscluster(kubernetes_cluster.kubectl,
                   cluster_name)

    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == capa_version
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"

    cleanup(kubernetes_cluster.kubectl)

@pytest.mark.smoke
def test_aws_cluster_policy_empty(kubernetes_cluster) -> None:
    cluster_name = "test-cluster-2"
    release_version = "20.0.0"
    capa_version = "capi"
    cluster_apps_operator_version = "2.0.0"

    ensure.release(kubernetes_cluster.kubectl, release_version,
                   cluster_apps_operator_version)
    ensure.cluster(kubernetes_cluster.kubectl,
                   cluster_name, release_version)
    ensure.awscluster(kubernetes_cluster.kubectl,
                   cluster_name)

    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == capa_version
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"

    cleanup(kubernetes_cluster.kubectl)


@pytest.mark.smoke
def test_aws_cluster_policy_solo(kubernetes_cluster) -> None:
    cluster_name = "test-cluster-3"
    capa_version = "capi"

    ensure.emptylabeledawscluster(kubernetes_cluster.kubectl,
                   cluster_name, capa_version)

    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == capa_version
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"

    cleanup(kubernetes_cluster.kubectl)

def cleanup(kubectl) -> None:
  kubectl("delete awscluster --all", output=None)
  kubectl("delete cluster --all", output=None)
  kubectl("delete release --all", output=None)

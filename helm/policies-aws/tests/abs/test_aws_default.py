import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import release
from ensure import cluster
from ensure import awscluster
from ensure import emptyawscluster
from ensure import emptylabeledawscluster
from ensure import awsclusterroleidentity

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_aws_cluster_policy(kubernetes_cluster, release, cluster, awscluster) -> None:
    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.capa_version
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"


@pytest.mark.smoke
def test_aws_cluster_policy_empty(kubernetes_cluster, release, cluster, emptyawscluster) -> None:
    assert emptyawscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.capa_version
    assert emptyawscluster['spec']['region'] == "eu-west-1"
    assert emptyawscluster['spec']['sshKeyName'] == "ssh-key"


@pytest.mark.smoke
def test_aws_cluster_policy_solo(kubernetes_cluster, emptylabeledawscluster) -> None:
    assert emptylabeledawscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.capa_version
    assert emptylabeledawscluster['spec']['region'] == "eu-west-1"
    assert emptylabeledawscluster['spec']['sshKeyName'] == "ssh-key"


@pytest.mark.smoke
def test_aws_cluster_role_identity_policy_solo(kubernetes_cluster, awsclusterroleidentity) -> None:
    assert awsclusterroleidentity['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.capa_version
    assert awsclusterroleidentity['spec']['sourceIdentityRef']['name'] == "default"
    assert awsclusterroleidentity['spec']['sourceIdentityRef']['kind'] == "AWSClusterControllerIdentity"

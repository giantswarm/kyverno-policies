import sys
sys.path.append('../../../tests')

import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import release
from ensure import cluster
from ensure import machinedeployment

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_cluster_policy(release, cluster) -> None:
    """
    test_cluster_policy tests defaulting of a Cluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release.
    """
    assert cluster['metadata']['labels']['cluster-apps-operator.giantswarm.io/version'] == ensure.cluster_apps_operator_version
    assert cluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label


@pytest.mark.smoke
def test_machine_deployment_policy(release, cluster, machinedeployment) -> None:
    """
    test_machine_deployment_policy tests defaulting of a MachineDeployment where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release.
    :param machinedeployment: MachineDeployment CR which is referenced by the Cluster.
    """
    assert machinedeployment['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label

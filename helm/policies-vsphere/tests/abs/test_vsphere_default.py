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
from ensure import vspherecluster
from ensure import vspherecluster_empty_labeled
from ensure import vspheremachinetemplate

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_vsphere_cluster_policy(release, cluster, vspherecluster) -> None:
    """
    test_vsphere_cluster_policy tests defaulting of an vsphereCluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the vsphereCluster.
    :param vspherecluster: vsphereCluster CR with empty strings which matches the Cluster CR.
    """
    assert vspherecluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label


@pytest.mark.smoke
def test_vsphere_cluster_policy_solo(vspherecluster_empty_labeled) -> None:
    """
    test_vsphere_cluster_policy_solo tests defaulting of an vsphereCluster where all required values are missing and no other CRs are given.

    :param vspherecluster_empty_labeled: vsphereCluster CR which is empty but has the cluster.x-k8s.io/watch-filter label.
    """
    assert vspherecluster_empty_labeled['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label

@pytest.mark.smoke
def test_vsphere_machine_template_policy_solo(vspheremachinetemplate) -> None:
    """
    test_vsphere_machine_template_policy_solo tests defaulting of an vsphereMachineTemplate where all required values are missing and no other CRs are given.

    :param vspheremachinetemplate: vsphereMachineTemplate CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """
    assert vspheremachinetemplate['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label

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
from ensure import vspherecluster

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_cluster_vsphere_policy(vspherecluster) -> None:
    """
    test_cluster_vsphere_policy tests defaulting of a controlPlaneEndpoints for vsphere clusters.

    :param vspherecluster: Factory for creation of Vsphere clusters.
    """
    # Pass in each cluster with the same endpoint
    cluster1 = vspherecluster('test1','192.0.0.1')
    cluster2 = vspherecluster('test2','192.0.0.1')
    cluster3 = vspherecluster('test3','192.0.0.1')
    assert cluster1['metadata']['name'] == 'test1'
    assert cluster2['metadata']['name'] == 'test2'
    assert cluster3['metadata']['name'] == 'test3'
    # Ensure endpoints are mutated to match values from values.yaml
    assert cluster1['spec']['controlPlaneEndpoint']['host'] == '1.1.1.1'
    assert cluster2['spec']['controlPlaneEndpoint']['host'] == '1.1.1.2'
    assert cluster3['spec']['controlPlaneEndpoint']['host'] == '1.1.1.3'


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
def test_cluster_vsphere_policy(release, vspherecluster) -> None:
    """
    test_cluster_policy tests defaulting of a Cluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    """
    cluster1 = vspherecluster('test','192.0.0.1')
    cluster2 = vspherecluster('test2','192.0.0.2')
    assert cluster1['metadata']['name'] == 'test'
    assert cluster2['metadata']['name'] == 'test2'
    assert release['metadata']['name'] == "v20.0.0"


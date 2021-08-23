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
from ensure import cluster_v1alpha4
from ensure import azurecluster

import pytest
from pytest_helm_charts import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_azure_cluster_policy(release, cluster_v1alpha4, azurecluster) -> None:
    """
    test_azure_cluster_policy tests defaulting of an AzureCluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AzureCluster.
    :param azurecluster: AzureCluster CR with empty strings which matches the Cluster CR.
    """
    assert azurecluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label

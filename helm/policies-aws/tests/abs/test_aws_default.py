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
from ensure import awscluster
from ensure import awscluster_empty
from ensure import awscluster_empty_labeled
from ensure import awsclusterroleidentity
from ensure import awsmachinetemplate

import pytest
from pytest_helm_charts import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_aws_cluster_policy(release, cluster, awscluster) -> None:
    """
    test_aws_cluster_policy tests defaulting of an AWSCluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster: AWSCluster CR with empty strings which matches the Cluster CR.
    """
    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"


@pytest.mark.smoke
def test_aws_cluster_policy_empty(release, cluster, awscluster_empty) -> None:
    """
    test_aws_cluster_policy_empty tests defaulting of an AWSCluster where all required values are missing.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster_empty: Empty AWSCluster CR which matches the Cluster CR.
    """
    assert awscluster_empty['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster_empty['spec']['region'] == "eu-west-1"
    assert awscluster_empty['spec']['sshKeyName'] == "ssh-key"


@pytest.mark.smoke
def test_aws_cluster_policy_solo(awscluster_empty_labeled) -> None:
    """
    test_aws_cluster_policy_solo tests defaulting of an AWSCluster where all required values are missing and no other CRs are given.

    :param awscluster_empty_labeled: AWSCluster CR which is empty but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awscluster_empty_labeled['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster_empty_labeled['spec']['region'] == "eu-west-1"
    assert awscluster_empty_labeled['spec']['sshKeyName'] == "ssh-key"


@pytest.mark.smoke
def test_aws_cluster_role_identity_policy_solo(awsclusterroleidentity) -> None:
    """
    test_aws_cluster_role_identity_policy_solo tests defaulting of an AWSClusterRoleIdentity where all required values are missing and no other CRs are given.

    :param awsclusterroleidentity: AWSClusterRoleIdentity CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awsclusterroleidentity['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awsclusterroleidentity['spec']['roleARN'] == "default-arn"
    assert awsclusterroleidentity['spec']['sourceIdentityRef']['name'] == "default"
    assert awsclusterroleidentity['spec']['sourceIdentityRef']['kind'] == "AWSClusterControllerIdentity"

@pytest.mark.smoke
def test_aws_machine_template_policy_solo(awsmachinetemplate) -> None:
    """
    test_aws_machine_template_policy_solo tests defaulting of an AWSMachineTemplate where all required values are missing and no other CRs are given.

    :param awsmachinetemplate: AWSMachineTemplate CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awsmachinetemplate['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awsmachinetemplate['spec']['template']['spec']['instanceType'] == "t3.large"

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
from ensure import awscluster_v1alpha3
from ensure import awscluster_v1alpha3_empty
from ensure import awscluster_v1alpha3_empty_labeled
from ensure import awsclusterroleidentity
from ensure import awsmachinetemplate
from ensure import awsmachinepool

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_aws_cluster_policy(release, cluster, awscluster_v1alpha3) -> None:
    """
    test_aws_cluster_policy tests defaulting of an AWSCluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster: AWSCluster CR with empty strings which matches the Cluster CR.
    """
    assert awscluster_v1alpha3['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster_v1alpha3['spec']['region'] == "eu-west-1"
    assert awscluster_v1alpha3['spec']['sshKeyName'] == "ssh-key"
    assert len(awscluster_v1alpha3['spec']['networkSpec']['cni']['cniIngressRules']) > 0


@pytest.mark.smoke
def test_aws_cluster_policy_empty(release, cluster, awscluster_v1alpha3_empty) -> None:
    """
    test_aws_cluster_policy_empty tests defaulting of an AWSCluster where all required values are missing.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster_empty: Empty AWSCluster CR which matches the Cluster CR.
    """
    assert awscluster_v1alpha3_empty['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster_v1alpha3_empty['spec']['region'] == "eu-west-1"
    assert awscluster_v1alpha3_empty['spec']['sshKeyName'] == "ssh-key"
    assert len(awscluster_v1alpha3_empty['spec']['networkSpec']['cni']['cniIngressRules']) > 0

@pytest.mark.smoke
def test_aws_cluster_policy_solo(awscluster_v1alpha3_empty_labeled) -> None:
    """
    test_aws_cluster_policy_solo tests defaulting of an AWSCluster where all required values are missing and no other CRs are given.

    :param awscluster_v1alpha3_empty_labeled: AWSCluster CR which is empty but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awscluster_v1alpha3_empty_labeled['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert awscluster_v1alpha3_empty_labeled['spec']['region'] == "eu-west-1"
    assert awscluster_v1alpha3_empty_labeled['spec']['sshKeyName'] == "ssh-key"
    assert len(awscluster_v1alpha3_empty_labeled['spec']['networkSpec']['cni']['cniIngressRules']) > 0

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

@pytest.mark.smoke
def test_aws_machine_pool_policy_solo(awsmachinepool) -> None:
    """
    test_aws_machine_pool_policy_solo tests defaulting of an AWSMachinePool where all required values are missing and no other CRs are given.

    :param awsmachinepool: AWSMachinePool CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """

    assert awsmachinepool['spec']['awsLaunchTemplate']['rootVolume']['size'] == 300
    assert awsmachinepool['spec']['awsLaunchTemplate']['rootVolume']['type'] == "gp3"

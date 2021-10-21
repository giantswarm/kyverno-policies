import pytest
import logging
import sys

sys.path.append('../../../tests')

# noinspection PyUnresolvedReferences
from ensure import (
    release,
    cluster,
    awscluster,
    awscluster_empty,
    awscluster_empty_labeled,
    awsclusterroleidentity,
    awsmachinetemplate,
    awsmachinepool,
    watch_label,
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_aws_cluster_policy(release, cluster, awscluster) -> None:
    """
    test_aws_cluster_policy tests defaulting of an AWSCluster where all required values are empty strings.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster: AWSCluster CR with empty strings which matches the Cluster CR.
    """
    assert awscluster['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == watch_label
    assert awscluster['spec']['region'] == "eu-west-1"
    assert awscluster['spec']['sshKeyName'] == "ssh-key"
    assert len(awscluster['spec']['networkSpec']['cni']['cniIngressRules']) > 0


@pytest.mark.smoke
def test_aws_cluster_policy_empty(release, cluster, awscluster_empty) -> None:
    """
    test_aws_cluster_policy_empty tests defaulting of an AWSCluster where all required values are missing.

    :param release: Release CR which is used by the Cluster.
    :param cluster: Cluster CR which uses the release and matches the AWSCluster.
    :param awscluster_empty: Empty AWSCluster CR which matches the Cluster CR.
    """
    assert awscluster_empty['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == watch_label
    assert awscluster_empty['spec']['region'] == "eu-west-1"
    assert awscluster_empty['spec']['sshKeyName'] == "ssh-key"
    assert len(awscluster_empty['spec']['networkSpec']['cni']['cniIngressRules']) > 0


@pytest.mark.smoke
def test_aws_cluster_policy_solo(awscluster_empty_labeled) -> None:
    """
    test_aws_cluster_policy_solo tests defaulting of an AWSCluster where all required values are missing and no other CRs are given.

    :param awscluster_empty_labeled: AWSCluster CR which is empty but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awscluster_empty_labeled['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == watch_label
    assert awscluster_empty_labeled['spec']['region'] == "eu-west-1"
    assert awscluster_empty_labeled['spec']['sshKeyName'] == "ssh-key"
    assert len(awscluster_empty_labeled['spec']['networkSpec']['cni']['cniIngressRules']) > 0


@pytest.mark.smoke
def test_aws_cluster_role_identity_policy_solo(awsclusterroleidentity) -> None:
    """
    test_aws_cluster_role_identity_policy_solo tests defaulting of an AWSClusterRoleIdentity where all required values are missing and no other CRs are given.

    :param awsclusterroleidentity: AWSClusterRoleIdentity CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awsclusterroleidentity['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == watch_label
    assert awsclusterroleidentity['spec']['roleARN'] == "default-arn"
    assert awsclusterroleidentity['spec']['sourceIdentityRef']['name'] == "default"
    assert awsclusterroleidentity['spec']['sourceIdentityRef']['kind'] == "AWSClusterControllerIdentity"


@pytest.mark.smoke
def test_aws_machine_template_policy_solo(awsmachinetemplate) -> None:
    """
    test_aws_machine_template_policy_solo tests defaulting of an AWSMachineTemplate where all required values are missing and no other CRs are given.

    :param awsmachinetemplate: AWSMachineTemplate CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """
    assert awsmachinetemplate['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == watch_label
    assert awsmachinetemplate['spec']['template']['spec']['instanceType'] == "t3.large"


@pytest.mark.smoke
def test_aws_machine_pool_policy_solo(awsmachinepool) -> None:
    """
    test_aws_machine_pool_policy_solo tests defaulting of an AWSMachinePool where all required values are missing and no other CRs are given.

    :param awsmachinepool: AWSMachinePool CR with empty strings but has the cluster.x-k8s.io/watch-filter label.
    """

    assert awsmachinepool['spec']['awsLaunchTemplate']['rootVolume']['size'] == 300
    assert awsmachinepool['spec']['awsLaunchTemplate']['rootVolume']['type'] == "gp3"

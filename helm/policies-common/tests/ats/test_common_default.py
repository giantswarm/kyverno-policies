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
from ensure import kubeadmconfig
from ensure import kubeadmconfig_controlplane
from ensure import kubeadmconfig_with_labels
from ensure import kubeadmconfig_with_role_labels
from ensure import kubeadmconfig_with_kubelet_args
from ensure import kubeadm_control_plane
from ensure import kubeadmconfig_controlplane
from ensure import kubeadmconfig_with_files
from ensure import kubeadmconfig_with_audit_file

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


@pytest.mark.smoke
def test_kubeadmconfig_policy(kubeadmconfig) -> None:
    """
    test_kubeadmconfig_policy tests defaulting of a KubeadmConfig where all required values are empty strings.

    :param kubeadmconfig: KubeadmConfig CR which is empty.
    """
    assert kubeadmconfig['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert kubeadmconfig['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['healthz-bind-address'] == "0.0.0.0"
    assert kubeadmconfig['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['v'] == "2"
    assert kubeadmconfig['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['image-pull-progress-deadline'] == "10m"
    assert kubeadmconfig['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['node-labels'] == "role=worker"

@pytest.mark.smoke
def test_kubeadmconfig_policy_with_labels(kubeadmconfig_with_labels) -> None:
    """
    test_kubeadmconfig_policy tests defaulting of a KubeadmConfig where all required values are empty strings.

    :param kubeadmconfig_with_labels: KubeadmConfig CR which is empty.
    """
    assert kubeadmconfig_with_labels['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert kubeadmconfig_with_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['healthz-bind-address'] == "0.0.0.0"
    assert kubeadmconfig_with_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['v'] == "2"
    assert kubeadmconfig_with_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['image-pull-progress-deadline'] == "10m"
    assert kubeadmconfig_with_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['node-labels'] == "role=worker,mylabel=test"

@pytest.mark.smoke
def test_kubeadmconfig_policy_with_role_labels(kubeadmconfig_with_role_labels) -> None:
    """
    test_kubeadmconfig_policy tests defaulting of a KubeadmConfig where all required values are empty strings.

    :param kubeadmconfig_with_role_labels: KubeadmConfig CR which is empty.
    """
    assert kubeadmconfig_with_role_labels['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert kubeadmconfig_with_role_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['healthz-bind-address'] == "0.0.0.0"
    assert kubeadmconfig_with_role_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['v'] == "2"
    assert kubeadmconfig_with_role_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['image-pull-progress-deadline'] == "10m"
    assert kubeadmconfig_with_role_labels['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['node-labels'] == "role=emperor,mylabel=test"

@pytest.mark.smoke
def test_kubeadmconfig_policy_with_kubelet_args(kubeadmconfig_with_kubelet_args) -> None:
    """
    test_kubeadmconfig_policy tests defaulting of a KubeadmConfig where all required values are empty strings.

    :param kubeadmconfig_with_kubelet_args: KubeadmConfig CR which is empty.
    """
    assert kubeadmconfig_with_kubelet_args['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert kubeadmconfig_with_kubelet_args['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['healthz-bind-address'] == "0.0.0.0"
    assert kubeadmconfig_with_kubelet_args['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['v'] == "1"
    assert kubeadmconfig_with_kubelet_args['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['image-pull-progress-deadline'] == "1m"
    assert kubeadmconfig_with_kubelet_args['spec']['joinConfiguration']['nodeRegistration']['kubeletExtraArgs']['node-labels'] == "role=worker"

@pytest.mark.smoke
def test_kubeadmconfig_policy_controlplane(kubeadmconfig_controlplane) -> None:
    """
    test_kubeadmconfig_policy_controlplane tests defaulting of a KubeadmConfig for a control plane where all required values are empty strings.

    :param kubeadmconfig_controlplane: KubeadmConfig CR which is empty.
    """
    assert kubeadmconfig_controlplane['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == ensure.watch_label
    assert kubeadmconfig_controlplane['metadata']['labels']['cluster.x-k8s.io/control-plane'] == ""
    # The object is completely empty before, so we make sure that it remains empty here.
    assert kubeadmconfig_controlplane.get('spec') is None

@pytest.mark.smoke
def test_kubeadmcontrolplane_policy(kubeadm_control_plane) -> None:
    """
    test_kubeadmconfig_policy_controlplane tests defaulting of a KubeadmConfig for a control plane where all required values are empty strings.

    :param kubeadmconfig_controlplane: KubeadmConfig CR which is empty.
    """
    assert kubeadm_control_plane['spec']['kubeadmConfigSpec']['initConfiguration']['nodeRegistration']['kubeletExtraArgs']['node-ip'] == '{{ ds.meta_data.local_ipv4 }}'
    assert kubeadm_control_plane['spec']['kubeadmConfigSpec']['clusterConfiguration']['apiServer']['extraArgs']['feature-gates'] == 'TTLAfterFinished=true'
    assert kubeadm_control_plane['spec']['kubeadmConfigSpec']['clusterConfiguration']['apiServer']['extraArgs']['runtime-config'] == 'api/all=true,scheduling.k8s.io/v1alpha1=true'

@pytest.mark.smoke
def test_kubeadmcontrolplane_auditpolicy(kubeadm_control_plane) -> None:
    """
    test_kubeadmcontrolplane_auditpolicy tests defaulting of a KubeadmControlPlane with audit policy details

    :param kubeadm_control_plane: KubeadmControlPlane CR which is empty.
    """
    assert kubeadm_control_plane['spec']['kubeadmConfigSpec']['clusterConfiguration']['apiServer']['extraArgs']['audit-policy-file'] == '/etc/kubernetes/policies/audit-policy.yaml'
    assert kubeadm_control_plane['spec']['kubeadmConfigSpec']['clusterConfiguration']['apiServer']['extraArgs']['audit-log-path'] == '/var/log/apiserver/audit.log'
    hasAuditPolicy = False
    hasLogPath = False
    for vol in kubeadm_control_plane['spec']['kubeadmConfigSpec']['clusterConfiguration']['apiServer']['extraVolumes']:
        if vol['hostPath'] == "/etc/kubernetes/policies":
            hasAuditPolicy = True
        if vol['hostPath'] == "/var/log/apiserver":
            hasLogPath = True
    assert hasAuditPolicy == True
    assert hasLogPath == True

@pytest.mark.smoke
def test_kubeadmconfig_auditpolicy(kubeadmconfig_with_files) -> None:
    """
    test_kubeadmconfig_auditpolicy tests defaulting of a kubeadmconfig with audit policy details

    :param kubeadmconfig_with_files: KubeadmConfig CR which includes some existing files
    """
    found = False
    for file in kubeadmconfig_with_files['spec']['files']:
        if file['path'] == "/etc/kubernetes/policies/audit-policy.yaml":
            found = True

    assert found == True

@pytest.mark.smoke
def test_kubeadmconfig_auditpolicy(kubeadmconfig_with_audit_file) -> None:
    """
    test_kubeadmconfig_auditpolicy tests defaulting of a kubeadmconfig with audit policy details

    :param kubeadmconfig_with_audit_file: KubeadmConfig CR which includes an existing audit file
    """
    assert len(kubeadmconfig_with_audit_file['spec']['files']) == 1


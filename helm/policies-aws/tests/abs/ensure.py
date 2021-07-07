import yaml
from functools import partial
import time
import random
import string
from textwrap import dedent

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)

cluster_name = "test-cluster"
release_version = "20.0.0"
cluster_apps_operator_version = "2.0.0"
capa_version = "capi"

@pytest.fixture(scope="module")
def release(kubernetes_cluster):
    r = dedent(f"""
        apiVersion: release.giantswarm.io/v1alpha1
        kind: Release
        metadata:
          creationTimestamp: null
          name: v{release_version}
        spec:
          apps:
          - name: calico
            version: 0.2.0
            componentVersion: 3.18.0
          - name: cert-exporter
            version: 1.6.0
          components:
          - name: cluster-api-bootstrap-provider-kubeadm
            version: 0.0.1
          - name: cluster-api-control-plane
            version: 0.0.1
          - name: cluster-api-core
            version: 0.0.1
          - name: cluster-api-provider-aws
            version: 0.0.1
          - name: cluster-apps-operator
            version: {cluster_apps_operator_version}
          date: "2021-03-22T14:50:41Z"
          state: active
        status:
          inUse: false
          ready: false
    """)

    kubernetes_cluster.kubectl("apply", input=r, output=None)
    LOGGER.info(f"Release v{release_version} applied")

    yield

    kubernetes_cluster.kubectl(f"delete release v{release_version}", output=None)
    LOGGER.info(f"Release v{release_version} deleted")

@pytest.fixture
def cluster(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: cluster.x-k8s.io/v1alpha3
        kind: Cluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            release.giantswarm.io/version: {release_version}
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
        spec:
          clusterNetwork:
            pods:
              cidrBlocks:
                - 192.168.0.0/16
          controlPlaneRef:
            apiVersion: controlplane.cluster.x-k8s.io/v1alpha3
            kind: KubeadmControlPlane
            name: {cluster_name}-control-plane
          infrastructureRef:
            apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
            kind: AWSCluster
            name: {cluster_name}
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"Cluster {cluster_name} applied")

    yield

    kubernetes_cluster.kubectl(f"delete cluster {cluster_name}", output=None)
    LOGGER.info(f"Cluster {cluster_name} deleted")

@pytest.fixture
def emptyawscluster(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AWSCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    yield awscluster

    kubernetes_cluster.kubectl(f"delete awscluster {cluster_name}", output=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")

@pytest.fixture
def emptylabeledawscluster(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AWSCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {capa_version}
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    yield awscluster

    kubernetes_cluster.kubectl(f"delete awscluster {cluster_name}", output=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")

@pytest.fixture
def awscluster(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AWSCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
        spec:
          region: ""
          sshKeyName: ""
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get awscluster {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    yield awscluster

    kubernetes_cluster.kubectl(f"delete awscluster {cluster_name}", output=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")

@pytest.fixture
def awsclusterroleidentity(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AWSClusterRoleIdentity
        metadata:
          labels:
            cluster.x-k8s.io/watch-filter: {capa_version}
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
          name: {cluster_name}
          namespace: default
        spec:
          allowedNamespaces:
            list:
            - org-marcel
          roleARN: ""
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AWSClusterRoleIdentity {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get AWSClusterRoleIdentity {cluster_name}", output="yaml")

    awsclusterroleidentity = yaml.safe_load(raw)

    yield awsclusterroleidentity

    kubernetes_cluster.kubectl(f"delete AWSClusterRoleIdentity {cluster_name}", output=None)
    LOGGER.info(f"AWSClusterRoleIdentity {cluster_name} deleted")

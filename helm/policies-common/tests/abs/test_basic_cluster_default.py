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


def ensure_release(kubectl, release_version, cluster_operator_version, capi_core_version):
    release = dedent(f"""
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
            version: {capi_core_version}
          - name: cluster-api-provider-aws
            version: 0.0.1
          - name: cluster-operator
            version: {cluster_operator_version}
          date: "2021-03-22T14:50:41Z"
          state: active
        status:
          inUse: false
          ready: false
    """)

    kubectl("apply", input=release, output=None)
    LOGGER.info(f"Release v{release_version} applied")


def ensure_cluster(kubectl, cluster_name, release_version):
    cluster = dedent(f"""
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

    kubectl("apply", input=cluster, output=None)
    LOGGER.info(f"Cluster {cluster_name} applied")


@pytest.mark.smoke
def test_cluster_policy(kubernetes_cluster) -> None:
    cluster_name = "test-cluster"
    release_version = "20.0.0-v1alpha3"
    capi_core_version = "0.0.2"
    cluster_operator_version = "2.0.0"

    obj = {}

    ensure_release(kubernetes_cluster.kubectl, release_version,
                   cluster_operator_version, capi_core_version)
    ensure_cluster(kubernetes_cluster.kubectl, cluster_name, release_version)

    raw = kubernetes_cluster.kubectl(
        f"get cluster {cluster_name}", output="yaml")

    obj = yaml.safe_load(raw)

    assert obj['metadata']['labels']['cluster-operator.giantswarm.io/version'] == cluster_operator_version
    assert obj['metadata']['labels']['cluster.x-k8s.io/watch-filter'] == capi_core_version

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


def ensure_release(kubectl):
    release = dedent("""
        apiVersion: release.giantswarm.io/v1alpha1
        kind: Release
        metadata:
          creationTimestamp: null
          name: v20.0.0-v1alpha3
        spec:
          components:
          - name: cluster-api-bootstrap-provider-kubeadm
            version: 0.0.1
          - name: cluster-api-control-plane
            version: 0.0.1
          - name: cluster-api-core
            version: 0.0.2
          - name: cluster-api-provider-aws
            version: 0.0.1
          - name: cluster-operator
            version: 3.6.2
          date: "2021-03-22T14:50:41Z"
          state: active
        status:
          inUse: false
          ready: false
    """)

    kubectl("apply", input=release, output=None)
    LOGGER.info(f"Release v20.0.0-v1alpha3 applied")


def ensure_cluster(kubectl, cluster_name):
    cluster = dedent(f"""
        apiVersion: cluster.x-k8s.io/v1alpha3
        kind: Cluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            release.giantswarm.io/version: 20.0.0-v1alpha3
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

    ensure_release(kubernetes_cluster.kubectl)
    ensure_cluster(kubernetes_cluster.kubectl, "test-cluster")

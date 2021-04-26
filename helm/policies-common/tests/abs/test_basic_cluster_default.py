from typing import cast

import pykube
import pytest
from pytest_helm_charts.clusters import Cluster


def ensure_release(kubectl):
    release = dedent("""
        apiVersion: release.giantswarm.io/v1alpha1
        kind: Release
        metadata:
          creationTimestamp: null
          name: v20.0.0-v1alpha3
        spec:
          apps:
          - name: calico
            version: 0.2.0
            componentVersion: 3.18.0
          components:
          - name: cluster-api-bootstrap-provider-kubeadm
            catalog: control-plane-test-catalog
            reference: 0.0.1
            releaseOperatorDeploy: true
            version: 0.0.1
          - name: cluster-api-control-plane
            catalog: control-plane-test-catalog
            reference: 0.0.1
            releaseOperatorDeploy: true
            version: 0.0.1
          - name: cluster-api-core
            catalog: control-plane-test-catalog
            reference: 0.0.2
            releaseOperatorDeploy: true
            version: 0.0.2
          - name: cluster-api-provider-aws
            catalog: control-plane-test-catalog
            reference: 0.0.1
            releaseOperatorDeploy: true
            version: 0.0.1
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

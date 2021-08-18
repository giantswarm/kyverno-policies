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

service_monitor_name = "test-service-monitor"
silence_name = "test-silence"
cluster_name = "test-cluster"
release_version = "20.0.0"
cluster_apps_operator_version = "2.0.0"
watch_label = "capi"

# Giant Swarm specific fixtures

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

# CAPI Core fixtures

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

    raw = kubernetes_cluster.kubectl(
        f"get cluster {cluster_name}", output="yaml")

    cluster = yaml.safe_load(raw)

    yield cluster

    kubernetes_cluster.kubectl(f"delete cluster {cluster_name}", output=None)
    LOGGER.info(f"Cluster {cluster_name} deleted")

@pytest.fixture
def machinedeployment(kubernetes_cluster):
    md = dedent(f"""
        apiVersion: cluster.x-k8s.io/v1alpha3
        kind: MachineDeployment
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
        spec:
          clusterName: {cluster_name}
          replicas: 1
          selector:
            matchLabels:
              clusterName: {cluster_name}
          template:
            spec:
              bootstrap:
                configRef:
                  apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
                  kind: KubeadmConfigTemplate
                  name: {cluster_name}
              clusterName: {cluster_name}
              infrastructureRef:
                apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
                kind: AWSMachineTemplate
                name: {cluster_name}
              version: v1.19.7
    """)

    kubernetes_cluster.kubectl("apply", input=md, output=None)
    LOGGER.info(f"MachineDeployment {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get machinedeployment {cluster_name}", output="yaml")

    machinedeployment = yaml.safe_load(raw)

    yield machinedeployment

    kubernetes_cluster.kubectl(f"delete machinedeployment {cluster_name}", output=None)
    LOGGER.info(f"MachineDeployment {cluster_name} deleted")

@pytest.fixture
def kubeadmconfig(kubernetes_cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
    """)

    kubernetes_cluster.kubectl("apply", input=md, output=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kubernetes_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")

# CAPA fixtures

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
def awscluster_empty(kubernetes_cluster):
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
def awscluster_empty_labeled(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AWSCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
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
def awsmachinetemplate(kubernetes_cluster):
    c = dedent(f"""
      apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
      kind: AWSMachineTemplate
      metadata:
        labels:
          cluster.x-k8s.io/cluster-name: {cluster_name}
          cluster.x-k8s.io/watch-filter: {watch_label}
          giantswarm.io/cluster: {cluster_name}
        name: {cluster_name}
        namespace: default
      spec:
        template:
          spec:
            iamInstanceProfile: control-plane-{cluster_name}
            sshKeyName: ""
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AWSMachineTemplate {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get AWSMachineTemplates {cluster_name}", output="yaml")

    awsmachinetemplate = yaml.safe_load(raw)

    yield awsmachinetemplate

    kubernetes_cluster.kubectl(f"delete AWSMachineTemplate {cluster_name}", output=None)
    LOGGER.info(f"AWSMachineTemplate {cluster_name} deleted")

@pytest.fixture
def awsclusterroleidentity(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AWSClusterRoleIdentity
        metadata:
          labels:
            cluster.x-k8s.io/watch-filter: {watch_label}
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

# CAPZ fixtures

@pytest.fixture
def azurecluster(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
        kind: AzureCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"AzureCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get azurecluster {cluster_name}", output="yaml")

    azurecluster = yaml.safe_load(raw)

    yield azurecluster

    kubernetes_cluster.kubectl(f"delete azurecluster {cluster_name}", output=None)
    LOGGER.info(f"AzureCluster {cluster_name} deleted")


# Silence fixtures

@pytest.fixture
def silence(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: monitoring.giantswarm.io/v1alpha1
        kind: Silence
        metadata:
          name: {silence_name}
          namespace: default
        spec:
          matchers: []
          targetTags: []
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"Silence {silence_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get silences {silence_name}", output="yaml")

    silence = yaml.safe_load(raw)

    yield silence

    kubernetes_cluster.kubectl(f"delete silence {silence_name}", output=None)
    LOGGER.info(f"Silence {silence_name} deleted")

@pytest.fixture
def silence_with_matchers(kubernetes_cluster):
    c = dedent(f"""
        apiVersion: monitoring.giantswarm.io/v1alpha1
        kind: Silence
        metadata:
          name: {silence_name}
          namespace: default
        spec:
          matchers:
          - isEqual: false
            isRegex: false
            name: test
            value: test
          targetTags: []
    """)

    kubernetes_cluster.kubectl("apply", input=c, output=None)
    LOGGER.info(f"Silence {silence_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get silences {silence_name}", output="yaml")

    silence = yaml.safe_load(raw)

    yield silence

    kubernetes_cluster.kubectl(f"delete silence {silence_name}", output=None)
    LOGGER.info(f"Silence {silence_name} deleted")


# Service Monitor fixtures

@pytest.fixture
def servicemonitor(kubernetes_cluster):
    sm = dedent(f"""
        apiVersion: monitoring.coreos.com/v1
        kind: ServiceMonitor
        metadata:
          name: {service_monitor_name}
          namespace: default
        spec:
          selector:
            matchLabels:
              app: my-app
          endpoints:
          - port: "web"
            relabelings:
              - targetLabel: app
          - port: "http"
            relabelings:
              - targetLabel: app
    """)

    kubernetes_cluster.kubectl("apply", input=sm, output=None)
    LOGGER.info(f"ServiceMonitor {service_monitor_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get servicemonitors {service_monitor_name}", output="yaml")

    serviceMonitor = yaml.safe_load(raw)

    yield serviceMonitor

    kubernetes_cluster.kubectl(f"delete servicemonitors {service_monitor_name}", output=None)
    LOGGER.info(f"ServiceMonitor {service_monitor_name} deleted")

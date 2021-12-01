import logging
from textwrap import dedent

import pytest
import yaml
from pytest_helm_charts.fixtures import Cluster

LOGGER = logging.getLogger(__name__)

service_monitor_name = "test-service-monitor"
silence_name = "test-silence"
cluster_name = "test-cluster"
machinepool_name = "mp0"
release_version = "20.0.0-alpha1"
cluster_apps_operator_version = "2.0.0"
watch_label = "capi"


# Giant Swarm specific fixtures

@pytest.fixture(scope="module")
def release(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=r, output_format=None)
    LOGGER.info(f"Release v{release_version} applied")

    raw = kube_cluster.kubectl(
        f"get release v{release_version}", output_format="yaml")

    release = yaml.safe_load(raw)

    yield release

    kube_cluster.kubectl(f"delete release v{release_version}", output_format=None)
    LOGGER.info(f"Release v{release_version} deleted")


# CAPI Core fixtures

@pytest.fixture
def cluster(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"Cluster {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get cluster {cluster_name}", output_format="yaml")

    cluster = yaml.safe_load(raw)

    yield cluster

    kube_cluster.kubectl(f"delete cluster {cluster_name}", output_format=None)
    LOGGER.info(f"Cluster {cluster_name} deleted")


@pytest.fixture
def cluster_v1alpha4(kube_cluster: Cluster):
    c = dedent(f"""
        apiVersion: cluster.x-k8s.io/v1alpha4
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
            apiVersion: controlplane.cluster.x-k8s.io/v1alpha4
            kind: KubeadmControlPlane
            name: {cluster_name}-control-plane
          infrastructureRef:
            apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
            kind: AWSCluster
            name: {cluster_name}
    """)

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"Cluster {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get cluster {cluster_name}", output_format="yaml")

    cluster = yaml.safe_load(raw)

    yield cluster

    kube_cluster.kubectl(f"delete cluster {cluster_name}", output_format=None)
    LOGGER.info(f"Cluster {cluster_name} deleted")


@pytest.fixture
def machinedeployment(kube_cluster: Cluster):
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
            metadata:
              labels:
                clusterName: {cluster_name}
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

    kube_cluster.kubectl("apply", std_input=md, output_format=None)
    LOGGER.info(f"MachineDeployment {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get machinedeployment {cluster_name}", output_format="yaml")

    machinedeployment = yaml.safe_load(raw)

    yield machinedeployment

    kube_cluster.kubectl(f"delete machinedeployment {cluster_name}", output_format=None)
    LOGGER.info(f"MachineDeployment {cluster_name} deleted")


@pytest.fixture
def kubeadmconfig(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=md, output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output_format="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kube_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")


@pytest.fixture
def kubeadmconfig_with_labels(kube_cluster: Cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
        spec:
          joinConfiguration:
            nodeRegistration:
              kubeletExtraArgs:
                node-labels: mylabel=test
    """)

    kube_cluster.kubectl("apply", std_input=md, output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output_format="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kube_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")


@pytest.fixture
def kubeadmconfig_with_files(kubernetes_cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
        spec:
          files:
          - content: ""
            encoding: base64
            owner: root
            path: /etc/ssh/sshd_config
            permissions: "640"
    """)

    kubernetes_cluster.kubectl("apply", input=md, output=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kubernetes_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")

@pytest.fixture
def kubeadmconfig_with_audit_file(kubernetes_cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
        spec:
          files:
          - content: ""
            encoding: base64
            owner: root
            path: /etc/kubernetes/policies/audit-policy.yaml
            permissions: "640"
    """)

    kubernetes_cluster.kubectl("apply", input=md, output=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kubernetes_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")

@pytest.fixture
def kubeadmconfig_with_role_labels(kube_cluster: Cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
        spec:
          joinConfiguration:
            nodeRegistration:
              kubeletExtraArgs:
                node-labels: role=emperor,mylabel=test
    """)

    kube_cluster.kubectl("apply", std_input=md, output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output_format="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kube_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")


@pytest.fixture
def kubeadmconfig_with_kubelet_args(kube_cluster: Cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
        spec:
          joinConfiguration:
            nodeRegistration:
              kubeletExtraArgs:
                v: "1"
                image-pull-progress-deadline: 1m
    """)

    kube_cluster.kubectl("apply", std_input=md, output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output_format="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kube_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")


@pytest.fixture
def kubeadmconfig_controlplane(kube_cluster: Cluster):
    md = dedent(f"""
        apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
        kind: KubeadmConfig
        metadata:
          name: {cluster_name}
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: {watch_label}
            cluster.x-k8s.io/control-plane: ""
    """)

    kube_cluster.kubectl("apply", std_input=md, output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get kubeadmconfig {cluster_name}", output_format="yaml")

    kubeadmconfig = yaml.safe_load(raw)

    yield kubeadmconfig

    kube_cluster.kubectl(f"delete kubeadmconfig {cluster_name}", output_format=None)
    LOGGER.info(f"KubeadmConfig {cluster_name} deleted")


# CAPA fixtures

@pytest.fixture
def awscluster_v1alpha3(kubernetes_cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get awsclusters.v1alpha3.infrastructure.cluster.x-k8s.io {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    yield awscluster

    kube_cluster.kubectl(f"delete awscluster {cluster_name}", output_format=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")


@pytest.fixture
def awscluster_v1alpha3_empty(kubernetes_cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get awsclusters.v1alpha3.infrastructure.cluster.x-k8s.io {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    yield awscluster

    kube_cluster.kubectl(f"delete awscluster {cluster_name}", output_format=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")


@pytest.fixture
def awscluster_v1alpha3_empty_labeled(kubernetes_cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AWSCluster {cluster_name} applied")

    raw = kubernetes_cluster.kubectl(
        f"get awsclusters.v1alpha3.infrastructure.cluster.x-k8s.io {cluster_name}", output="yaml")

    awscluster = yaml.safe_load(raw)

    yield awscluster

    kube_cluster.kubectl(f"delete awscluster {cluster_name}", output_format=None)
    LOGGER.info(f"AWSCluster {cluster_name} deleted")


@pytest.fixture
def awsmachinetemplate(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AWSMachineTemplate {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get AWSMachineTemplates {cluster_name}", output_format="yaml")

    awsmachinetemplate = yaml.safe_load(raw)

    yield awsmachinetemplate

    kube_cluster.kubectl(f"delete AWSMachineTemplate {cluster_name}", output_format=None)
    LOGGER.info(f"AWSMachineTemplate {cluster_name} deleted")


@pytest.fixture
def awsmachinepool(kube_cluster: Cluster):
    c = dedent(f"""
      apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
      kind: AWSMachinePool
      metadata:
        labels:
          cluster.x-k8s.io/cluster-name: {cluster_name}
          cluster.x-k8s.io/watch-filter: capi
          giantswarm.io/cluster: {cluster_name}
          giantswarm.io/machine-pool: {cluster_name}
        name: {cluster_name}
        namespace: default
      spec:
        availabilityZones:
        - eu-west-1a
        awsLaunchTemplate:
          iamInstanceProfile: nodes-{cluster_name}-{cluster_name}
          instanceType: m5.xlarge
          sshKeyName: ""
        maxSize: 2
        minSize: 2
    """)

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AWSMachinePool {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get AWSMachinePools {cluster_name}", output_format="yaml")

    awsmachinepool = yaml.safe_load(raw)

    yield awsmachinepool

    kube_cluster.kubectl(f"delete AWSMachinePool {cluster_name}", output_format=None)
    LOGGER.info(f"AWSMachinePool {cluster_name} deleted")


@pytest.fixture
def awsclusterroleidentity(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AWSClusterRoleIdentity {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get AWSClusterRoleIdentity {cluster_name}", output_format="yaml")

    awsclusterroleidentity = yaml.safe_load(raw)

    yield awsclusterroleidentity

    kube_cluster.kubectl(f"delete AWSClusterRoleIdentity {cluster_name}", output_format=None)
    LOGGER.info(f"AWSClusterRoleIdentity {cluster_name} deleted")


# CAPZ fixtures

@pytest.fixture
def azurecluster(kube_cluster: Cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha4
        kind: AzureCluster
        metadata:
          name: {cluster_name}
          namespace: default
          labels:
            giantswarm.io/cluster: {cluster_name}
            cluster.x-k8s.io/cluster-name: {cluster_name}
        spec:
          location: ""
    """)

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AzureCluster {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get azurecluster {cluster_name}", output_format="yaml")

    azurecluster = yaml.safe_load(raw)

    yield azurecluster

    kube_cluster.kubectl(f"delete azurecluster {cluster_name}", output_format=None)
    LOGGER.info(f"AzureCluster {cluster_name} deleted")


@pytest.fixture
def azuremachinepool(kube_cluster: Cluster):
    c = dedent(f"""
        apiVersion: infrastructure.cluster.x-k8s.io/v1alpha4
        kind: AzureMachinePool
        metadata:
          name: {machinepool_name}
          namespace: default
          labels:
            "cluster.x-k8s.io/cluster-name": {cluster_name}
            "giantswarm.io/cluster": {cluster_name}
        spec:
          identity: SystemAssigned
          location: ""
          strategy:
            rollingUpdate:
              deletePolicy: Oldest
              maxSurge: 25%
              maxUnavailable: 1
            type: RollingUpdate
          template:
            osDisk:
              diskSizeGB: 30
              managedDisk:
                storageAccountType: Premium_LRS
              osType: Linux
            sshPublicKey: ""
            vmSize: Standard_D4s_v3
    """)

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"AzureMachinePool {machinepool_name} applied")

    raw = kube_cluster.kubectl(
        f"get AzureMachinePool {machinepool_name}", output_format="yaml")

    azuremachinepool = yaml.safe_load(raw)

    yield azuremachinepool

    kube_cluster.kubectl(f"delete azuremachinepool {machinepool_name}", output_format=None)
    LOGGER.info(f"AzureMachinePool {machinepool_name} deleted")


# Silence fixtures

@pytest.fixture
def silence(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"Silence {silence_name} applied")

    raw = kube_cluster.kubectl(
        f"get silences {silence_name}", output_format="yaml")

    silence = yaml.safe_load(raw)

    yield silence

    kube_cluster.kubectl(f"delete silence {silence_name}", output_format=None)
    LOGGER.info(f"Silence {silence_name} deleted")


@pytest.fixture
def silence_with_matchers(kube_cluster: Cluster):
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

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"Silence {silence_name} applied")

    raw = kube_cluster.kubectl(
        f"get silences {silence_name}", output_format="yaml")

    silence = yaml.safe_load(raw)

    yield silence

    kube_cluster.kubectl(f"delete silence {silence_name}", output_format=None)
    LOGGER.info(f"Silence {silence_name} deleted")


@pytest.fixture
def kubeadm_control_plane(kube_cluster: Cluster):
    c = dedent(f"""
        apiVersion: controlplane.cluster.x-k8s.io/v1alpha4
        kind: KubeadmControlPlane
        metadata:
          labels:
            cluster.x-k8s.io/cluster-name: {cluster_name}
            cluster.x-k8s.io/watch-filter: capi
          name: {cluster_name}
          namespace: default
        spec:
          kubeadmConfigSpec:
            clusterConfiguration:
              apiServer:
                extraArgs:
                  cloud-config: /etc/kubernetes/azure.json
                  cloud-provider: azure
                extraVolumes:
                - hostPath: /etc/kubernetes/azure.json
                  mountPath: /etc/kubernetes/azure.json
                  name: cloud-config
                  readOnly: true
              controllerManager:
                extraArgs:
                  allocate-node-cidrs: "false"
          machineTemplate:
            infrastructureRef:
              apiVersion: infrastructure.cluster.x-k8s.io/v1alpha4
              kind: AWSMachineTemplate
              name: {cluster_name}
          version: 1.22.0
    """)

    kube_cluster.kubectl("apply", std_input=c, output_format=None)
    LOGGER.info(f"KubeadmControlPlane {cluster_name} applied")

    raw = kube_cluster.kubectl(
        f"get kubeadmcontrolplane {cluster_name}", output_format="yaml")

    kcp = yaml.safe_load(raw)

    yield kcp

    kube_cluster.kubectl(f"delete kubeadmcontrolplane {cluster_name}", output_format=None)
    LOGGER.info(f"kubeadmcontrolplane {cluster_name} deleted")

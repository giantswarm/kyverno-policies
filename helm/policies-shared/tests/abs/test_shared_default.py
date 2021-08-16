import sys
sys.path.append('../../../tests')

import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import silence
from ensure import servicemonitor

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
def test_silence_heartbeat_policy(silence) -> None:
    """
    test_silence_heartbeat_policy tests defaulting of an empty Silence to check for the negative Heartbeat matcher.

    :param silence: Any Silence CR.
    """
    matchers = silence['spec']['matchers']

    for matcher in matchers:
        if matcher['name'] == "alertname":
            assert (matcher['value'] == "Heartbeat" and not matcher['isRegex'] and not matcher['isEqual'])
            return

    pytest.fail("Heartbeat matcher is missing")


@pytest.mark.smoke
def test_service_monitor_labelling_schema_policy(servicemonitor) -> None:
    """
    test_service_monitor_labelling_schema_policy tests defaulting of an empty Service monitor to check that the labelling schema is configured.

    :param servicemonitor: Any ServiceMonitor CR.
    """
    endpoints = servicemonitor['spec']['endpoints']
    for endpoint in endpoints:
        relabelings = endpoint['relabelings']
        assert relabelings[0]['replacement'] == '' and relabelings[0]['targetLabel'] == 'cluster_id'                                      \
          and relabelings[1]['replacement'] == 'management_cluster' and relabelings[1]['targetLabel'] == 'cluster_type'                   \
          and relabelings[2]['replacement'] == '' and relabelings[2]['targetLabel'] == 'provider'                                         \
          and relabelings[3]['replacement'] == '' and relabelings[3]['targetLabel'] == 'installation'                                     \
          and relabelings[4]['sourceLabels'] == ['__meta_kubernetes_namespace'] and relabelings[4]['targetLabel'] == 'namespace'          \
          and relabelings[5]['sourceLabels'] == ['__meta_kubernetes_pod_name'] and relabelings[5]['targetLabel'] == 'pod'                 \
          and relabelings[6]['sourceLabels'] == ['__meta_kubernetes_pod_container_name'] and relabelings[6]['targetLabel'] == 'container' \
          and relabelings[7]['sourceLabels'] == ['__meta_kubernetes_pod_node_name'] and relabelings[7]['targetLabel'] == 'node'           \
          and relabelings[8]['sourceLabels'] == ['__meta_kubernetes_node_label_role'] and relabelings[8]['targetLabel'] == 'role'         \
          and relabelings[9]['sourceLabels'] == ['__meta_kubernetes_node_label_role'] and relabelings[9]['targetLabel'] == 'role'         \
          and relabelings[9]['regex'] == '' and relabelings[9]['replacement'] == 'worker'                                                 \
        , 'Invalid relabelings {}'.format(relabelings)
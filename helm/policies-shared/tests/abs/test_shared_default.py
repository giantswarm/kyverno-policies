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
        assert len(relabelings) > 0, 'Invalid relabelings {}'.format(relabelings)

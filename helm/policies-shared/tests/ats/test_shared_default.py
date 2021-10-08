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
from ensure import silence_with_matchers

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
def test_silence_heartbeat_policy_with_existing_matchers(silence_with_matchers) -> None:
    """
    test_silence_heartbeat_policy tests defaulting of a Silence container a matcher to check for the negative Heartbeat matcher.

    :param silence_with_matchers: Any Silence CR container a matcher.
    """
    matchers = silence_with_matchers['spec']['matchers']

    assert (matchers[0]['value'] == "test" and matchers[0]['name'] == "test" and not matchers[0]['isRegex'] and not matchers[0]['isEqual'])
    assert (matchers[1]['value'] == "Heartbeat" and matchers[1]['name'] == "alertname" and not matchers[1]['isRegex'] and not matchers[1]['isEqual'])

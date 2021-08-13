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

    for i, v in enumerate(matchers):
        if v['name'] == "alertname":
            assert (v['value'] == "Heartbeat" and not v['isRegex'] and not v['isEqual'])
            return

    pytest.fail("Heartbeat matcher is missing")

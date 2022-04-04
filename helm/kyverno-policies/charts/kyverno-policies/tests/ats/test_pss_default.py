import sys
sys.path.append('../../../../tests')

import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import release
from ensure import cluster
from ensure import awscluster_v1alpha3
from ensure import awscluster_v1alpha3_empty
from ensure import awscluster_v1alpha3_empty_labeled
from ensure import awsclusterroleidentity
from ensure import awsmachinetemplate
from ensure import awsmachinepool

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
def test_empty_test() -> None:
    return

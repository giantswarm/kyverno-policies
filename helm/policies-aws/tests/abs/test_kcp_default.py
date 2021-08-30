import sys
sys.path.append('../../../tests')

from functools import partial
import time
import string

from ensure import kubeadm_control_plane

import pytest

import logging
LOGGER = logging.getLogger(__name__)


@pytest.mark.smoke
def test_kcp_allocate_node_cidrs(kubeadm_control_plane) -> None:
    """
    test_kcp_allocate_node_cidrs tests the `allocate_node_cidrs` is set to true.

    :param kubeadm_control_plane: KubeadmControlPlane CR created from an empty spec.
    """
    assert kubeadm_control_plane['spec']['kubeadmConfigSpec']['clusterConfiguration']['controllerManager']['extraArgs']['allocate-node-cidrs'] == "true"

import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service(host):
    s = host.service("smokeping_prober")
    # assert s.is_enabled
    assert s.is_running


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9374")
    assert s.is_listening

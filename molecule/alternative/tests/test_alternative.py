import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/smokeping_prober.service",
    "/usr/local/bin/smokeping_prober"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'


def test_user(host):
    assert host.group("smokeping_prober").exists
    assert host.user("smokeping_prober").exists


def test_service(host):
    s = host.service("smokeping_prober")
    # assert s.is_enabled
    assert s.is_running


def test_socket(host):
    s = host.socket("tcp://127.0.0.1:9000")
    assert s.is_listening

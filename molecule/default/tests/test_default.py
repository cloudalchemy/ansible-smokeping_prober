import pytest
import os
import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleDefaults():
    with open("../../defaults/main.yml", 'r') as stream:
        return yaml.load(stream)


@pytest.mark.parametrize("dirs", [
    "/etc/prometheus",
    "/etc/prometheus/console_libraries",
    "/etc/prometheus/consoles",
    "/etc/prometheus/rules",
    "/etc/prometheus/file_sd",
    "/var/lib/prometheus"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


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
    s = host.socket("tcp://0.0.0.0:9374")
    assert s.is_listening


def test_version(host, AnsibleDefaults):
    version = os.getenv('PROMETHEUS',
                        AnsibleDefaults['smokeping_prober_version'])
    out = host.run("/usr/local/bin/smokeping_prober --version").stderr
    assert "smokeping_prober, version " + version in out

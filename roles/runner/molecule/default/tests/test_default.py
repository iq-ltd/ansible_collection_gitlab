import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_gitlab_runner_package(host):
    """The GitLab runner package is installed"""
    gitlab_runner_package = host.package("gitlab-runner")
    assert gitlab_runner_package.is_installed


@pytest.mark.parametrize(
    "command", ("gitlab-runner status", "gitlab-runner health-check")
)
def test_gitlab_runner_health(host, command):
    """GitLab runner is healthy."""
    host.run_test(command)

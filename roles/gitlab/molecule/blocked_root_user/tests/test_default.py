import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

GITLAB_EDITION = os.getenv("GITLAB_EDITION")


def test_root_user_blocked(host):
    """Root user is blocked"""
    root_user_status = host.run(
        """gitlab-rails runner 'user = User.find(1); puts user.attributes["state"]'"""
    ).stdout.strip()
    assert root_user_status == "blocked"

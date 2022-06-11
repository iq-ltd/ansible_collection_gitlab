import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

GITLAB_EDITION = os.getenv("GITLAB_EDITION")


login_test_script = """
import requests
from bs4 import BeautifulSoup

gitlab_url = "{url}"
gitlab_user = "{user}"
gitlab_password = "{password}"
with requests.Session() as session:
    session.verify = False
    sign_in_get = session.get(gitlab_url + "/users/sign_in")
    sign_in_html = BeautifulSoup(sign_in_get.content, "html.parser")
    authenticity_token = sign_in_html.find("input", {{"name":"authenticity_token"}})["value"]
    login_payload = {{
       "authenticity_token": authenticity_token,
       "user[login]": gitlab_user,
       "user[password]": gitlab_password,
       "user[remember_me]": "0"
    }}
    login_post = session.post(gitlab_url + "/users/sign_in", login_payload, allow_redirects=False)
    assert login_post.status_code == {expected_status}
"""


def test_gitlab_package(host):
    """The right GitLab package is installed"""
    if GITLAB_EDITION == "enterprise":
        gitlab_package = host.package("gitlab-ee")
    elif GITLAB_EDITION == "community":
        gitlab_package = host.package("gitlab-ce")
    else:
        raise TypeError(
            f"GITLAB_EDITION can either be enterprise or community, not {GITLAB_EDITION}"
        )
    assert gitlab_package.is_installed


@pytest.mark.parametrize("command", ("gitlab-ctl status", "gitlab-rake gitlab:check"))
def test_gitlab_health(host, command):
    """GitLab healthcheck commands run with a return code of 0."""
    host.run_test(command)


def test_gitlab_nginx(host):
    """GitLab login path returns 200 with GitLab in content."""
    gitlab_url = host.ansible.get_variables()["gitlab_external_url"]
    signin_page_request = host.ansible(
        "ansible.builtin.uri",
        f"url={gitlab_url}/users/sign_in follow_redirects=none force=true return_content=true validate_certs=false",
        check=False,
    )
    assert signin_page_request["status"] == 200
    assert "GitLab" in signin_page_request["content"]


def test_registry_nginx(host):
    """Registry API returns 401."""
    gitlab_registry_url = host.ansible.get_variables()["gitlab_registry_external_url"]
    registry_request = host.ansible(
        "ansible.builtin.uri",
        f"url={gitlab_registry_url}/v2/ follow_redirects=none force=true return_content=true validate_certs=false",
        check=False,
    )
    assert registry_request["status"] == 401


def test_root_user_id(host):
    """Root user has id 1"""
    user_1 = host.run(
        """gitlab-rails runner 'user = User.find(1); puts user.attributes["name"]; puts user.attributes["username"]'"""
    ).stdout.splitlines()
    user_1_name = user_1[0]
    user_1_username = user_1[1]
    assert user_1_name == "Administrator"
    assert user_1_username == "root"


def test_root_user_not_blocked(host):
    """Root user isn't blocked"""
    root_user_status = host.run(
        """gitlab-rails runner 'user = User.find(1); puts user.attributes["state"]'"""
    ).stdout
    assert isinstance(root_user_status, str)
    assert root_user_status != "blocked"


def test_valid_root_user_password(host):
    """Correct root user password allows login"""
    password = host.ansible.get_variables()["gitlab_root_user_password"]
    host.run("python3 -m pip install requests bs4")
    formatted_script = login_test_script.format(
        url="https://git.example.com",
        user="root",
        password=password,
        expected_status=302,
    )
    script = host.run(f"echo '{formatted_script}' | python3")
    assert script.rc == 0


def test_invalid_root_user_password(host):
    """Incorrect root user password does not allow login"""
    host.run("python3 -m pip install requests bs4")
    formatted_script = login_test_script.format(
        url="https://git.example.com",
        user="root",
        password="IncorrectPassword",
        expected_status=200,
    )
    script = host.run(f"echo '{formatted_script}' | python3")
    assert script.rc == 0


def test_signup_disabled(host):
    """Signup is disabled"""
    signup_enabled = (
        host.run("echo 'select signup_enabled from application_settings' | gitlab-psql")
        .stdout.splitlines()[2]
        .strip()
    )
    print(signup_enabled)
    assert signup_enabled == "f"

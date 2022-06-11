# GitLab Ansible Colletion

Ansible collection with roles to install GitLab community edition, enterprise edition and GitLab runners.

## Roles

| Role                | Description                                              |
| ------------------- | -------------------------------------------------------- |
| initq.gitlab.ce     | Install and configure GitLab Omnibus Community Edition.  |
| initq.gitlab.ee     | Install and configure GitLab Omnibus Enterprise Edition. |
| initq.gitlab.runner | Install a GitLab runner.                                 |

## Variables

### initq.gitlab.ce / initq.gitlab.ee

| Variable                                  | Required | Default | Input                        | Comments                                                                                                                               |
| ----------------------------------------- | -------- | ------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| gitlab_external_url                       | **yes**  | _null_  | `str`                        | GitLab URL.                                                                                                                            |
| gitlab_disable_signup                     | no       | `false` | `bool`                       | Disable user sign-up.<br />⚠️ Reactivating signup has to be done using the GUI in addition to setting this variable to `false`.        |
| gitlab_root_user_password                 | no       | _null_  | `str`                        | GitLab root user password.                                                                                                             |
| gitlab_root_user_blocked                  | no       | `false` | `bool`                       | Block GitLab root user.<br />⚠️ Unblocking the root user has to be done using the GUI in addition to setting this variable to `false`. |
| gitlab_nginx_listen_addresses             | no       | _null_  | `list[str, ...]`             | GitLab NGINX listen addresses. If none are defined only unix sockets will be created in '/run/gitlab'.                                 |
| gitlab_nginx_ssl_certificate              | no       | _null_  | `str`                        | Path to GitLab SSL certificate.                                                                                                        |
| gitlab_nginx_ssl_certificate_key          | no       | _null_  | `str`                        | Path to GitLab SSL private key.                                                                                                        |
| gitlab_registry_nginx_listen_addresses    | no       | _null_  | `list[str, ...]`             | GitLab registry NGINX listen addresses. If none are defined only unix sockets will be created in '/run/gitlab'.                        |
| gitlab_registry_nginx_listen_port         | no       | _null_  | `int`                        | GitLab registry NGINX listen port.                                                                                                     |
| gitlab_registry_nginx_ssl_certificate     | no       | _null_  | `str`                        | Path to GitLab registry SSL certificate.                                                                                               |
| gitlab_registry_nginx_ssl_certificate_key | no       | _null_  | `str`                        | Path to GitLab registry SSL private key.                                                                                               |
| gitlab_letsencrypt_enable                 | no       | `false` | `bool`                       | Manage certificates automatically using LetsEncrypt.                                                                                   |
| gitlab_registry_enable                    | no       | `true`  | `bool`                       | Enable GitLab container registry site-wide.                                                                                            |
| gitlab_registry_external_url              | no       | _null_  | `str`                        | GitLab container registry URL.                                                                                                         |
| gitlab_smtp_enable                        | no       | `false` | `bool`                       | Enable GitLab SMTP.                                                                                                                    |
| gitlab_smtp_address                       | no       | _null_  | `str`                        | GitLab SMTP server address.                                                                                                            |
| gitlab_smtp_port                          | no       | `465`   | `int`                        | GitLab SMTP server port.                                                                                                               |
| gitlab_smtp_user_name                     | no       | _null_  | `str`                        | GitLab SMTP server user name.                                                                                                          |
| gitlab_smtp_user_password                 | no       | _null_  | `str`                        | GitLab SMTP server user password.                                                                                                      |
| gitlab_smtp_domain                        | no       | _null_  | `str`                        | GitLab SMTP domain.                                                                                                                    |
| gitlab_smtp_authentication                | no       | _null_  | `str` (`"login"`, `"plain"`) | GitLab SMTP authentication.                                                                                                            |
| gitlab_smtp_enable_starttls_auto          | no       | _null_  | `bool`                       | Enable SMTP starttls.                                                                                                                  |
| gitlab_smtp_tls                           | no       | _null_  | `bool`                       | Enable SMTP TLS.                                                                                                                       |
| gitlab_email_from                         | no       | _null_  | `str`                        | GitLab Email address that will be used to send Email.                                                                                  |
| gitlab_email_display_name                 | no       | _null_  | `str`                        | GitLab Email display name.                                                                                                             |

### initq.gitlab.runner

| Variable                             | Required | Default             | Input            | Comments                                                                       |
| ------------------------------------ | -------- | ------------------- | ---------------- | ------------------------------------------------------------------------------ |
| gitlab_runner_ci_server_url          | **yes**  | _null_              | `str`            | GitLab runner CI server URL.                                                   |
| gitlab_runner_registration_token     | **yes**  | _null_              | `str`            | GitLab runner CI server registration token.                                    |
| gitlab_runner_tags                   | no       | _null_              | `list[str, ...]` | GitLab runner tags.                                                            |
| gitlab_runner_executor               | no       | `"docker"`          | `str`            | GitLab runner executor.                                                        |
| gitlab_runner_run_untagged           | no       | `false`             | `bool`           | Run untagged jobs.                                                             |
| gitlab_runner_limit                  | no       | `<number of cores>` | `int`            | Maximum number of builds processed by the runner. Defaults to number of cores. |
| gitlab_runner_docker_image           | no       | `"ubuntu:latest"`   | `str`            | The default Docker image to run jobs with.                                     |
| gitlab_runner_docker_privileged      | no       | `false`             | `bool`           | Run job containers in privileged mode.                                         |
| gitlab_runner_docker_runtime         | no       | _null_              | `str`            | The runtime for Docker containers.                                             |
| gitlab_runner_allow_custom_build_dir | no       | `true`              | `bool`           | Allow user to define a custom build directory for a job.                       |

## Example Playbook

```yaml
- hosts: gitlab_ce
  roles:
    - initq.gitlab.ce
  vars:
    gitlab_external_url: "https://git.example.com"
    gitlab_letsencrypt_enable: true
    gitlab_disable_signup: true
    gitlab_root_user_password: "TopSecretPassword!"

- hosts: gitlab_runners
  roles:
    - initq.gitlab.runner
  vars:
    gitlab_runner_ci_server_url: "https://git.example.com"
    gitlab_runner_registration_token: "Eyohzaemaiso1ahshahj6Ohpeigh2g"
```

## License

[GNU General Public License v3.0](./LICENSE)

## Author Information

Marvin Vogt (git@srv6d.space)

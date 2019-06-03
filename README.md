# Ansible role: RabbitMQ

[![Build Status](https://travis-ci.org/mbaran0v/ansible-rabbitmq.svg?branch=master)](https://travis-ci.org/mbaran0v/ansible-rabbitmq) [![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT) [![GitHub tag](https://img.shields.io/github/tag/mbaran0v/ansible-rabbitmq.svg)](https://github.com/mbaran0v/ansible-rabbitmq/tags/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Ansible role for install and configure [RabbitMQ message broker](https://www.rabbitmq.com). Currently this works on Debian and RedHat based linux systems. Supports standalone or simple cluster deployment, it is based on [abelboldu.rabbitmq](https://github.com/abelboldu/ansible-rabbitmq) role.

Tested platforms are:

* Ubuntu 16.04
* CentOS 7

Requirements
------------

Requires EPEL repository for RHEL/CentOS; recommended role for EPEL installation: [geerlingguy.repo-epel](https://github.com/geerlingguy/ansible-role-repo-epel)

Role Variables
--------------

### Environment

Use `rabbitmq_conf_env` so set Environment variables such as NODENAME,
HOSTNAME, RABBITMQ_USE_LONGNAME, NODE_PORT, NODE_IP_ADDRESS, etc.

Example:

```yaml
rabbitmq_conf_env:
  NODENAME: rabbit1

```

### Configuration file

`rabbitmq_tcp_address` - listening address for the tcp interface, such
as `0.0.0.0`.

`rabbitmq_tcp_port` - listening port for the tcp interface, such as `5672`.

`rabbitmq_cluster` - a boolean variable, when set to `True` the role will add
all nodes in a play group to a cluster setup in a configuration file. It
depends on a `ansible_play_hosts` magic variable, found in ansible 2.2
or later.

`rabbitmq_erlang_cookie` - only used when `rabbitmq_cluster` is used, to
identify members of a single cluster.

### Plugins

`rabbitmq_plugins` - list of plugins to activate.

### Users

`rabbitmq_users` - list of users, and associated vhost and password.
Example on defining the users configuration:

```yaml
rabbitmq_users:
  - user:     user1
    password: password1             # Optional, defaults to ""
    vhost:    vhost1                # Optional, defaults to "/"
    node:     node_name             # Optional, defaults to "rabbit"
    configure_priv: "^resource.*"   # Optional, defaults to ".*"
    read_priv: "^$"                 # Disallow reading (defaults to ".*")
    write_priv: "^$"                # Disallow writing (defaults to ".*")
  - user:     user2
    password: password2
    vhost:    vhost1
    force:    no
    tags:                           # Optional, user tags
    - administrator
  - user:     guest
    state:    absent                # Optional, removes user (defaults to "present")
```

### Vhosts

`rabbitmq_vhosts` - list of vhosts to create. Example on defining the
vhosts configuration:

```yaml
rabbitmq_vhosts:
  - name:     vhost1
    node:     node_name             # Optional, defaults to "rabbit"
    tracing:  yes                   # Optional, defaults to "no"
    state:    present               # Optional, defaults to "present"
```

### Policies

`rabbitmq_policies` - list of policies to be created (or removed if
`state: absent` is set). Example on defining the policies configuration:

```yaml
rabbitmq_policies:
  - name:     HA Policy
    vhost:    '/'                   # Optional, defaults to "/"
    pattern:  '.*'                  # Optional, defaults to ".*"
    tags:                           # Optional, defaults to "{}"
      ha-mode: all
      ha-sync-mode: automatic
    state:    present               # Optional, defaults to "present"
```

### Cluster setup

This role supports setting up a simple cluster by adding all the nodes in a
play group that uses the role. It adds the nodes to `cluster_nodes` section
in rabbitmq.conf file. All the nodes are `disc` nodes. The role also sets the
same "Erlang Cookie" to all the nodes belonging to a cluster. In this way
nodes join the cluster automatically during the bootstrap.

For the initial deployment, it is advised to serialize the node deployment in
a way that, at first, a single node is deployed, followed by all the other
nodes in the second run. This would result in a consistent cluster setup.
Playbook example:

```yaml
  - hosts: rabbitmq
    become: True
    serial:
      - 1
      - '100%'
    roles:
      - rabbitmq
```

### File descriptors

`rabbitmq_fd_limit` - set this to some numeric value to override 1024
default. Currently only supports systemd.

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- hosts: rabbitmq
  roles:
    - role: geerlingguy.repo-epel
      when: ansible_os_family == 'RedHat'
    - role: mbaran0v.rabbitmq
```

License
-------

BSD

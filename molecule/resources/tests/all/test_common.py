
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


def test_distribution(host):
    assert host.system_info.distribution.lower() in debian_os + rhel_os


def test_service(host):
    s = host.service('rabbitmq-server')

    assert s.is_enabled
    assert s.is_running

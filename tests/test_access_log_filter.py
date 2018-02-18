import os
from nose.tools import raises, assert_raises
from nose.tools import with_setup, ok_, eq_
from ipaddress import IPv4Network, IPv6Network
from access_log_filter.access_log_filter import (
    AccessLog,
    IpFilter
)

fixtures_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures'
)

class TestAccessLog(object):
    def setup(self):
        with open(os.path.join(fixtures_dir, 'valid_small_access_log.txt')) as f:
            self.valid_small_access_log = f.read().splitlines()

        with open(os.path.join(fixtures_dir, 'invalid_small_access_log.txt')) as f:
            self.invalid_small_access_log = f.read().splitlines() 

    @raises(FileNotFoundError)
    def test_nonexistent_file_raises_file_not_found(self):
        AccessLog('nonexistentfile')

    @with_setup(setup)
    def test_tokenize_capture_all_groups_with_valid_record(self):
        access_log = AccessLog(
            os.path.join(
                fixtures_dir, 'valid_small_access_log.txt')
        )

        for record in self.valid_small_access_log:
            a = access_log._tokenize(record)
            eq_(len(a.groups()), 13)

    @with_setup(setup)
    def test_tokenize_return_none_type_with_bad_schema_line(self):
        access_log = AccessLog(
            os.path.join(
                fixtures_dir, 'invalid_small_access_log.txt')
        )

        for record in self.invalid_small_access_log:
            a = access_log._tokenize(record)
            ok_(isinstance(a, type(None)))

    def test_filter_return_correct_number_of_lines(self):
        access_log = AccessLog(
            os.path.join(
                fixtures_dir, 'valid_small_access_log.txt')
        )
        eq_(len(list(access_log.filter_it(IpFilter('31.184.238.128')))), 1)
        eq_(len(list(access_log.filter_it(IpFilter('157.55.39.180')))), 2)
        eq_(len(list(access_log.filter_it(IpFilter('127.0.0.1')))), 0)

    def test_filter_return_no_line_with_invalid_ip(self):
        access_log = AccessLog(
            os.path.join(
                fixtures_dir, 'invalid_ip_small_access_log.txt')
        )
        eq_(len(list(access_log.filter_it(IpFilter('31.184.238.128')))), 0)
        eq_(len(list(access_log.filter_it(IpFilter('157.55.39.180')))), 0)
        eq_(len(list(access_log.filter_it(IpFilter('127.0.0.1')))), 0)


class TestIpFilter(object):
    def setup(self):
        with open(os.path.join(fixtures_dir, 'invalid_addr.txt')) as f:
            self.invalid_addr = f.read().splitlines()

        with open(os.path.join(fixtures_dir, 'valid_addr.txt')) as f:
            self.valid_addr = f.read().splitlines()

        with open(os.path.join(fixtures_dir, 'addr_within_cdir.txt')) as f:
            self.addr_within_cdir = f.read().splitlines()

        with open(os.path.join(fixtures_dir, 'addr_not_in_cdir.txt')) as f:
            self.addr_not_in_cdir = f.read().splitlines()

    @with_setup(setup)
    def test_init_raises_value_error_with_invalid_ip_cdir_value(self):
        for addr in self.invalid_addr:
            assert_raises(ValueError, IpFilter, addr)

    @with_setup(setup)
    def test_network_return_good_class_obj_with_valid_ip_cdir_value(self):
        def valid_network(network):
            return (
                isinstance(network, IPv4Network)
                or
                isinstance(network, IPv6Network)
            )

        for addr in self.valid_addr:
            ok_(valid_network(IpFilter(addr).network))
            ok_(valid_network(IpFilter(addr).network)) # Using setter method

    def test_match_returns_false_for_ip_not_in_cdir(self):
        for addr in self.addr_not_in_cdir:
            ip, network = addr.split(',')
            print(network, ip)
            eq_(IpFilter(network).match(ip), False)

    def test_match_returns_true_for_ip_within_cdir(self):
        for addr in self.addr_within_cdir:
            ip, network = addr.split(',')
            print(network, ip)
            eq_(IpFilter(network).match(ip), True)

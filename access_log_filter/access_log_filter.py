"""
This file holds the classes used by the access_log_filter package
"""
import re
from ipaddress import ip_address, ip_network


class AccessLog(object):
    """"
    Represents the access log file and the lines schema, which
    is tokenized using a regular expression, filter() using
    filter objects for specific attributes such as contained ips
    """
    def __init__(self, path):
        """
        Check that access_log file is readable and holds the
        regular expression that defined the access_log schema
        """
        with open(path):
            pass

        self.path = path
        self._access_log_regex = ''.join([
            '(?P<ip>.*?) ',
            '(?P<ident>.*?) ',
            '(?P<user_id>.*?) ',
            '\[(?P<date>.*?)(?= ) ',
            '(?P<timezone>.*?)\] ',
            '"(?P<request_method>.*?) (?P<path>.*?)(?P<request_version> HTTP/.*)?" ',
            '(?P<status>.*?) ',
            '(?P<length>.*?) '
            '"(?P<referrer>.*?)" ',
            '"(?P<user_agent>.*?)" ',
            '"(?P<virtual_host>.*?)"'
        ])

    def _tokenize(self, _string):
        """
        Tokenize the access_log file lines using regular expression schema
        Returns a tuple with all 'tokens' or None
        """
        return re.search(self._access_log_regex, _string)

    def filter_it(self, _filter):
        """
        Returns a python generator that yields filtered lines
        of the whole access_log file using the filter
        object argument
        """
        with open(self.path) as _file:
            for line in _file:
                tokens = self._tokenize(line)
                if tokens:
                    _ip = tokens.group('ip')
                    if _filter.match(_ip):
                        yield line


class IpFilter(object):
    """
    IpFilter object is used to match
    ip network and addresses overlap, initialize it with a CDIR network
    and then use match with an ip address to see if it's contained within
    """
    def __init__(self, value):
        """ip accepts ipv4, ipv6 and CDIR notation"""
        self._network = self._to_network(value)

    @staticmethod
    def _to_network(value):
        return ip_network(value)

    @property
    def network(self):
        """Return the instantiated CDIR network"""
        return self._network

    @network.setter
    def network(self, value):
        self._network = self._to_network(value)

    def match(self, _ip):
        """
        Return True if the ip argument is contained within the
        initialized CDIR network
        """
        try:
            return bool(ip_address(_ip) in self.network)
        except ValueError:
            return False

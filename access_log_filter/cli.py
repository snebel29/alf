"""
Access Log Filter (alf)

Usage:
  alf <access_log> --ip=<ip_address>
  alf -h | --help
  alf -v | --version

Options:
  -i IP, --ip=IP     Filter by ip, ipv4, ipv6 and CDIR notation allowed
  -h, --help         Show the help
  -v, --version      Show version

Examples:
  alf access_log --ip 127.0.0.1
  alf access_log --ip ::1
  alf access_log --ip 10.0.0.0/8
  alf access_log --ip 2001:db8::/128
"""

import sys
from ipaddress import ip_network
from docopt import docopt
from schema import Schema, SchemaError, Use
from access_log_filter import AccessLog, IpFilter, __version__


def _validate(args):
    Schema({
        '--help': bool,
        '--version': bool,
        '<access_log>': Use(open),
        '--ip': Use(ip_network)
    }).validate(args)

def _parse_args(args):
    return docopt(__doc__, args, version=__version__)

def _filter_strings(_list):
    return [w for w in _list if isinstance(w, str)]

def run(args=None):
    """Entry point for alf tool"""
    if args is None:
        args = sys.argv[1:]

    args = _parse_args(args)
    try:
        _validate(args)
    except SchemaError as exc:
        sys.stderr.write(' '.join(_filter_strings(exc.autos)))
        sys.exit(1)

    access_log = AccessLog(args['<access_log>'])
    filtered = access_log.filter_it(
        IpFilter(args['--ip'])
    )

    for line in filtered:
        sys.stdout.write(line)

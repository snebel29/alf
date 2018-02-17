import os
from schema import SchemaError
from unittest.mock import patch
from nose.tools import raises, assert_raises
from nose.tools import with_setup, ok_, eq_
from access_log_filter.cli import (
    run,
    _validate,
    _parse_args,
    _filter_strings,
)


class TestCli(object):

    def setup(self):
        self.access_log_file = 'access_log'
        self.valid_argv = [self.access_log_file, '--ip', '127.0.0.1']
        self.valid_arg_dict = {
            '--help': False,
            '--version': False,
            '<access_log>': self.access_log_file,
            '--ip': '127.0.0.1'
        }
        with open(self.access_log_file, 'w'):
            pass

    def teardown(self):
        os.remove(self.access_log_file)


    @raises(SystemExit)
    def test_parse_args_with_no_arguments_should_system_exit(self):
        _parse_args([])

    @raises(SystemExit) 
    def test_parse_without_access_log_argument_should_system_exit(self):
        argv = ['--ip', '127.0.0.1']
        _parse_args(argv)

    @raises(SystemExit) 
    def test_parse_with_bad_flag_argument_should_system_exit(self):
        argv = ['access_log', '--pi', '127.0.0.1']
        _parse_args(argv)

    @raises(SystemExit) 
    def test_parse_without_ip_argument_value_should_system_exit(self):
        argv = ['access_log', '--ip']
        _parse_args(argv)

    @with_setup(setup, teardown)
    def test_parse_args_with_valid_arguments_should_parse(self):
        args = _parse_args(self.valid_argv)

        ok_(isinstance(args, dict))
        eq_(args['--help'], False)
        eq_(args['--version'], False)
        eq_(args['--ip'], '127.0.0.1')
        eq_(args['<access_log>'], 'access_log')

    def test_validate_args_with_incomplete_structure_should_schema_error(self):
        assert_raises(SchemaError, _validate, {'--ip': '127.0.0.1'})
        assert_raises(SchemaError, _validate, {'--help2': True})
        assert_raises(SchemaError, _validate, {'--invalidFlag': True})
        assert_raises(SchemaError, _validate, {'<myFile>': self.access_log_file})

    @with_setup(setup, teardown)
    def test_validate_args_with_invalid_address_should_schema_error(self):
        args_dict_bad_addr = self.valid_arg_dict
        bad_addr = [
            '127.0.0.256',
            '127.0.-1',
            '2003::dead:beef:4dad:23:46:bb:101',
            '2003:beef:4dad:23:46:bb:101',
            '10.0.0.0/33',
            '10.0.0/8',
            '2001::::/18',
            '2001:db8::/129'
        ]

        for bad_addr in bad_addr:
            args_dict_bad_addr['--ip'] = bad_addr
            assert_raises(SchemaError, _validate, args_dict_bad_addr)

    @with_setup(setup, teardown)
    def test_validate_args_with_valid_address_works(self):
        args_dict_good_addr = self.valid_arg_dict
        good_addreses = [
            '10.0.0.0/8',
            '2001::/18',
            '2001:db8::/128',
            '::1',
            '127.0.0.1',
            '192.168.0.1'
        ]

        for good_addr in good_addreses:
            args_dict_good_addr['--ip'] = good_addr
            _validate(args_dict_good_addr)

    @raises(SchemaError)
    def test_validate_args_with_nonexistent_file_schema_error(self):
        arg_dict_with_nonexistent_file = self.valid_arg_dict
        arg_dict_with_nonexistent_file['<access_log>'] = 'nonexistent'
        _validate(arg_dict_with_nonexistent_file)

    def test_filter_strings(self):
        eq_(_filter_strings([True, None, 'a', 1]), ['a'])
        eq_(_filter_strings(['a', 'b', 'c']), ['a', 'b', 'c'])
        eq_(_filter_strings([{}, (1,), [], SchemaError, 'a']), ['a'])
    

    @patch('access_log_filter.cli._parse_args')
    @patch('access_log_filter.cli._validate')
    @patch('access_log_filter.cli.AccessLog')
    @with_setup(setup, teardown)
    def test_run_parse_validate_and_filter(
        self, 
        mock_access_log,
        mock_validate,
        mock_parse_args
    ):

        run(self.valid_argv)
        ok_(mock_parse_args.called)
        ok_(mock_validate.called)
        ok_(mock_access_log.called)

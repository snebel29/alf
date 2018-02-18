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

fixtures_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures'
)

class TestCli(object):
    def setup(self):
        self.ip = '127.0.0.1'
        self.access_log_file = 'access_log'
        self.valid_argv = [self.access_log_file, '--ip', self.ip]
        self.valid_arg_dict = {
            '--help': False,
            '--version': False,
            '<access_log>': self.access_log_file,
            '--ip': self.ip
        }
        with open(self.access_log_file, 'w'):
            # Dummy access_log blank file
            pass

        with open(os.path.join(fixtures_dir, 'invalid_addr.txt')) as f:
            self.invalid_addr = f.read().splitlines()

        with open(os.path.join(fixtures_dir, 'valid_addr.txt')) as f:
            self.valid_addr = f.read().splitlines()

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
        args_dict_invalid_addr = self.valid_arg_dict

        for invalid_addr in self.invalid_addr:
            args_dict_invalid_addr['--ip'] = invalid_addr
            assert_raises(SchemaError, _validate, args_dict_invalid_addr)

    @with_setup(setup, teardown)
    def test_validate_args_with_valid_address_works(self):
        args_dict_valid_addr = self.valid_arg_dict

        for valid_addr in self.valid_addr:
            args_dict_valid_addr['--ip'] = valid_addr
            _validate(args_dict_valid_addr)

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
    @patch('access_log_filter.cli.AccessLog.filter_it')
    @patch('access_log_filter.cli.IpFilter')
    @with_setup(setup, teardown)
    def test_run_parse_validate_and_filter(
            self,
            mock_ip_filter,
            mock_access_log_filter,
            mock_validate,
            mock_parse_args
    ):

        run(self.valid_argv)
        ok_(mock_parse_args.called)
        ok_(mock_validate.called)
        ok_(mock_access_log_filter.called)

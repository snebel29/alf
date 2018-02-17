from setuptools import setup
from access_log_filter import __version__


requirements = ['docopt', 'schema']
dev_requirements = ['nose']

setup(
    name='access-log-filter',
    packages=['access_log_filter'],
    version=__version__,
    description='A simple access_log filter CLI tool written in python',
    author='Sven Nebel',
    author_email='nebel.sven@gmail.com',
    author_github='https://github.com/snebel29',
    license='MIT',
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'alf=access_log_filter.cli:run',
            'access_log_filter=access_log_filter.cli:run'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
    ]
)
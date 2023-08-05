# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microlib']

package_data = \
{'': ['*'], 'microlib': ['data/*']}

install_requires = \
['blessed>=1.18.1,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'intspan>=1.6.1,<2.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_full_version >= "3.7.0" and python_full_version < "3.8.0"': ['importlib-metadata>=3.1,<5.0']}

setup_kwargs = {
    'name': 'microlib',
    'version': '1.9.2',
    'description': 'Collection of various useful tools.',
    'long_description': '|coveralls|\n\nLicense\n=======\nMicrolib is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or any later version. See LICENSE file.\n\nMicrolib also includes third party open source software components: the Deprecated class. It has its own license. Please see ./microlib/deprecation.py\n\nOverview\n========\n\nMicrolib contains some useful functions or classes:\n\n- XDict is a dict with recursive_update() and flat() methods,\n- StandardConfigFile helps to manage user config files,\n- terminal.ask_yes_no() and terminal.ask_user_choice() to ask questions to the user for cli tools,\n- terminal.tabulate() is a very simple function to display tabulated data in the terminal,\n- terminal.echo_info() echo_warning() and echo_error() display info, warning and error messages with some color.\n- rotate() and grouper() help to handle iterators.\n- database offers a ContextManager for sqlite3 database, an Operator and a Ts_Operator classes to provide shortcuts for common sqlite3 commands.\n- a Deprecated class, that provides a decorator to deprecate functions (emit a warning when it is called).\n\n`Source code <https://gitlab.com/nicolas.hainaux/microlib>`__\n\n.. |coveralls| image:: https://coveralls.io/repos/gitlab/nicolas.hainaux/microlib/badge.svg?branch=master\n  :target: https://coveralls.io/gitlab/nicolas.hainaux/microlib?branch=master\n',
    'author': 'Nicolas Hainaux',
    'author_email': 'nh.techn@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nicolas.hainaux/microlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plugin_mongo', 'tests']

package_data = \
{'': ['*']}

modules = \
['pyproject']
install_requires = \
['dep-spec==0.3.6', 'motor>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'dep-plugin-mongo',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'everhide',
    'author_email': 'i.tolkachnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

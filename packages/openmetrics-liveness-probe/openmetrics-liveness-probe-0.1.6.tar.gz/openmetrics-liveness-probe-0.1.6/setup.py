# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openmetrics_liveness_probe']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client>=0.9', 'pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'openmetrics-liveness-probe',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Daniil Nikitin',
    'author_email': 'dnikitin@usetech.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)

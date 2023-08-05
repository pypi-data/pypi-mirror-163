# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_parse_time',
 'fast_parse_time.bp',
 'fast_parse_time.dmo',
 'fast_parse_time.dto',
 'fast_parse_time.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'natural-time', 'openpyxl', 'pandas', 'tabulate']

setup_kwargs = {
    'name': 'fast-parse-time',
    'version': '0.1.2',
    'description': 'Natural Language (NLP) Extraction of Date and Time',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)

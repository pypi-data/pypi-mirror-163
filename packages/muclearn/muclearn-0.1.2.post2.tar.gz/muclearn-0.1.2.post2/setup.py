# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['muclearn', 'muclearn..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['holidays>=0.14.2,<0.15.0',
 'pandas>=1.4,<2.0',
 'requests>=2,<3',
 'scikit-learn>=1,<2']

setup_kwargs = {
    'name': 'muclearn',
    'version': '0.1.2.post2',
    'description': 'A collection of helpers and tools for machine learning.',
    'long_description': '# muclearn\n\nThis is a small collection of helpers and tools for machine learning in Python.\nIt currently mainly focuses on Pandas and dates, but will be expanded in the future.',
    'author': 'Fabian Reinold',
    'author_email': 'fabian.reinold@muenchen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

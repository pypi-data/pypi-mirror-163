# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymbse',
 'pymbse.pymbse',
 'pymbse.pymbse.config',
 'pymbse.pymbse.model_api',
 'pymbse.pymbse.model_api.executor',
 'pymbse.pymbse.model_api.snapshot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'nbconvert>=6.5.0,<7.0.0',
 'papermill>=2.3.4,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pymbse-commons>=0.0.6,<0.0.7',
 'scrapbook>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'pymbse',
    'version': '0.0.12',
    'description': '',
    'long_description': None,
    'author': 'mmaciejewski',
    'author_email': 'michal.maciejewski@ief.ee.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

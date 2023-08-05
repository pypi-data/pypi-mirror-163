# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_gcp', 'django_gcp.events', 'django_gcp.storage']

package_data = \
{'': ['*'], 'django_gcp': ['static/*', 'templates/django_gcp/*']}

install_requires = \
['Django>=3.0,<4.0',
 'django-app-settings>=0.7.1,<0.8.0',
 'gcp-pilot>=0.40.0,<0.41.0',
 'google-auth>=2.6.0,<3.0.0',
 'google-cloud-storage>=2.1.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'django-gcp',
    'version': '0.5.0',
    'description': 'Utilities to run Django on Google Cloud Platform',
    'long_description': "[![PyPI version](https://badge.fury.io/py/django_gcp.svg)](https://badge.fury.io/py/django_gcp)\n[![codecov](https://codecov.io/gh/octue/django-gcp/branch/main/graph/badge.svg?token=H2QLSCF3DU)](https://codecov.io/gh/octue/django-gcp)\n[![Documentation](https://readthedocs.org/projects/django_gcp/badge/?version=latest)](https://django_gcp.readthedocs.io/en/latest/?badge=latest)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n# DjangoGCP\n\nHelps you to run Django on Google Cloud Platform - Storage, PubSub and Tasks.\n\nRead the [documentation here](https://django_gcp.readthedocs.io/en/latest).\n\nThis app is maintained by Octue - we're on a mission to help climate scientists and energy engineers be more efficient. [Find out more](https://www.octue.com).\n\nIf you need some help implementing or updating this, we can help! Raise an issue or [contact us](https://www.octue.com/contact).\n\n## Are you from GCP??\n\nIf so, get in touch for a chat. We're doing fun things with Google Cloud. Way funner than boring old django... :)\n\n## All the :heart:\n\nThis app is based heavily on [django-storages](https://django-storages.readthedocs.io/en/latest/), [django-google-cloud-tasks](https://github.com/flamingo-run/django-cloud-tasks) and uses the [django-rabid-armadillo](https://github.com/thclark/django-rabid-armadillo) template. Big love.\n\n## Contributing\n\nIt's pretty straightforward to get going, but it's good to get in touch first, especially if you're planning a big feature.\n\nOpen the project in codespaces, a vscode .devcontainer or your favourite IDE or editor (if the latter you'll need to set up docker-compose yourself), then:\n\n```\npoetry install\n```\n\nRun the tests:\n\n```\npytest .\n```\n\nWe use pre-commit to ensure code quality standards (and to help us automate releases using conventional-commits). If you can get on board with this that's really helpful - if not, don't fret, we can help.\n",
    'author': 'Tom Clark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/octue/django-gcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

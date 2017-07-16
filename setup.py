# -*- coding: utf-8 -*-

import os

from setuptools import setup

__here__ = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(__here__, 'README.rst')).read()
REQUIREMENTS = [
    i.strip()
    for i in open(os.path.join(__here__, 'requirements.txt')).readlines()
]

# Get VERSION
version_file = os.path.join('verboselib', 'version.py')
# Use exec for compabibility with Python 3
exec(open(version_file).read())


setup(
    name='verboselib',
    version=VERSION,
    description='A little L10N framework for libraries and applications',
    long_description=README,
    keywords=[
        'library', 'l10n', 'localization', 'lazy', 'string', 'framework',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/oblalex/verboselib',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    license='LGPLv3',
    packages=[
        'verboselib',
        'verboselib.management',
        'verboselib.management.commands',
    ],
    entry_points={
        'console_scripts': [
            'verboselib-manage = verboselib.bin.verboselib_manage:main',
        ],
    },
    platforms=[
        'any',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
)

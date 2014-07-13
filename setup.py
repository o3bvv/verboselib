# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()

name = 'verboselib'
requirements = [
    r.strip() for r in open(os.path.join(here, 'requirements.txt')).readlines()
]

exec(open(os.path.join(here, name, 'version.py')).read())

setup(
    name=name,
    version=__version__,
    description='L10N support for stand-alone libraries',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/oblalex/verboselib',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    license='LGPLv3',
    packages=[
        'verboselib',
        'verboselib.bin',
        'verboselib.management',
    ],
    scripts=[
        'verboselib/bin/verboselib-manage.py',
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)

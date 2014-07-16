verboselib
==========

|Build Status| |Coverage Status| |PyPi package| |PyPi downloads|

A little L10N framework for Python libraries and applications.

**Table of contents**

.. contents::
    :local:
    :depth: 1
    :backlinks: none

Keypoints
---------

``verboselib`` can help you to add verbosity to stand-alone libraries or
applications. This includes:

- support of usual and lazy translatable messages;
- support of setting and disabling current active language at runtime for
  current thread for all libraries and modules which use ``verboselib``;
- tools to help you to update and compile catalogs of translations.

In short, all this looks like `translation in Django`_ but without Django.

    A samurai without a sword is like a samurai with one, but only without one.

Installation
------------

Install from `PyPI <https://pypi.python.org/pypi/verboselib>`_:

.. code-block:: bash

    $ pip install verboselib

Usage
-----

Managing
--------

Changelog
---------

Credits
-------

Future plans and thoughts
-------------------------

.. |Build Status| image:: http://img.shields.io/travis/oblalex/verboselib.svg?style=flat&branch=master
   :target: https://travis-ci.org/oblalex/verboselib
.. |Coverage Status| image:: http://img.shields.io/coveralls/oblalex/verboselib.svg?style=flat&branch=master
   :target: https://coveralls.io/r/oblalex/verboselib?branch=master
.. |PyPi package| image:: http://img.shields.io/pypi/v/verboselib.svg?style=flat
   :target: http://badge.fury.io/py/verboselib/
.. |PyPi downloads| image::  http://img.shields.io/pypi/dm/verboselib.svg?style=flat
   :target: https://crate.io/packages/verboselib/

.. _translation in Django: https://docs.djangoproject.com/en/1.7/topics/i18n/translation/

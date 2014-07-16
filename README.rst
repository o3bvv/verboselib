verboselib
==========

|Build Status| |Coverage Status| |PyPi package| |PyPi downloads|

A little L10N framework for Python libraries and applications.

**Table of contents**

.. contents::
    :local:
    :depth: 1
    :backlinks: none

Key points
---------

``verboselib`` can help you to add verbosity to stand-alone libraries or
applications. This includes:

- support of usual and lazy translatable messages;
- support of setting and disabling current active language at runtime for
  current thread globally;
- tools to help you to update and compile catalogs of translations.

In short, all this looks like `translation in Django`_, but without Django.

    A samurai without a sword is like a samurai with one, but only without one.

Installation
------------

Install from `PyPI <https://pypi.python.org/pypi/verboselib>`_:

.. code-block:: bash

    $ pip install verboselib

API overview
------------

Here's a quick usage example:

.. code-block:: python

    >>> from verboselib import use_language
    >>> from verboselib.factory import TranslationsFactory

    >>> translations = TranslationsFactory(domain="example", locale_dir="locale")
    >>> _ = translations.ugettext_lazy

    >>> message = _("Hi there!")
    >>> use_language('en')
    >>> print(message)
    'Hi there!'
    >>> use_language('sv')
    >>> print(message)
    'Hej där!'

TranslationsFactory
^^^^^^^^^^^^^^^^^^^

The key point here is usage of an instance of a ``TranslationsFactory`` class
called ``translations``. You need to use its methods to make translatable
messages. This is done to make sure your translations are really initialized,
that they are initialized only once and stored in a single place only.

    **TIP**: instantiate ``TranslationsFactory`` at some convenient place
    (e.g. top-level ``__init__.py``, ``utils.py``, ``translations.py`` or any
    other place you like). Then you will be able to import that instance from
    any other module, e.g.:

    .. code-block:: python

        from .utils import translations

To create an instance of a ``TranslationsFactory`` class you need to tell a
``domain`` name and path to directory, where your translation catalogs are
stored (``locale_dir``).

    **TIP**: to keep things simple you can

    1. set domain name same as the name of your library, application or just
       a package;
    2. place ``locale_dir`` at the top level of your package;

..

    **STRONG RECOMMENDATION**: tell the absolute path of your ``locale_dir``
    while instantiating your translations. This is especially vital if you are
    going to distribute a public library. Example:

    .. code-block:: python

      # Example '__init__.py'

      import os
      from verboselib.factory import TranslationsFactory


      here = os.path.abspath(os.path.dirname(__file__))
      locale_dir = os.path.join(here, "locale")
      translations = TranslationsFactory("example", locale_dir)

So, you want to get your translated messages. There some way to do that. List
of currently supported methods includes:

- ``gettext`` - get a localized translation of message, based on the global
  language in current thread;
- ``ugettext`` - same as ``gettext``, but returns translated message as a
  Unicode string (equal to ``gettext`` for Python 3);
- ``gettext_lazy`` - get a lazy translation of message, will be evaluated in
  future accordingly to the global language in current thread;
- ``ugettext_lazy`` same as ``gettext_lazy``, but returns evaluated message as a
  Unicode string (equal to ``gettext_lazy`` for Python 3);

..

    **TIP**: Don't be afraid to use different aliases for different translation
    methods, e.g.:

    .. code-block:: python

      from .utils import translations

      _, U_ = translations.gettext, translations.ugettext
      L_, UL_ = translations.gettext_lazy, translations.ugettext_lazy

Setting up default language
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are developing some application, it makes sence to specify a **global**
default language. This language will be used if current language is not
specified. Example:

.. code-block:: python

  from verboselib import set_default_language

  set_default_language('en')

..

    **TIP**: set default language somewhere near the place you instantiate the
    ``TranslationsFactory`` class at.

If both current and default languages are not set, original messages will be
returned instead of their translations.

Setting up current language
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can set up current **global** language for current thread from any place:

.. code-block:: python

  from verboselib import use_language

  use_language('fr')

Querying current language
^^^^^^^^^^^^^^^^^^^^^^^^^

You can get the value of currently used language:

.. code-block:: python

  from verboselib import get_language

  get_language()

If current value is ``None``, this means that neither current nor default
language is set and original messages will be returned.

Clearing current language
^^^^^^^^^^^^^^^^^^^^^^^^^

You can clear the value of current **global** language, so next translations
will use default language:

.. code-block:: python

  from verboselib import drop_language

  drop_language()

..

    **TIP**: sometimes it makes sence to restore previous language instead of
    dropping it, e.g.:

    .. code-block:: python

      from verboselib import get_language, use_language
      from .utils import translations

      _ = translations.ugettext


      def send_greeting_email(user):
        saved = get_language()
        use_language(user.language)

        subject = _("Welcome to our service")
        message = _("Hello, {:}! Glad to see you among our users!").format(user.first_name)

        use_language(saved)
        send_email(subject, message, user.email)

Disabling translations
^^^^^^^^^^^^^^^^^^^^^^

If you wish, you can totally disable translations, so original messages will be
used:

.. code-block:: python

  from verboselib import use_language_bypass

  use_language_bypass()

After this ``get_language`` function will return ``None``.

Use ``use_language`` to enable translations again.

Locale-to-language conversions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``verboselib`` comes up with a couple of hepler function for converting language
to locale:

.. code-block:: python

  >>> from verboselib.heplers import to_locale
  >>> to_locale('en-us')
  'en_US'
  >>> to_locale('en-us', to_lower=True)
  'en_us'

and vice versa, for converting locale to language:

.. code-block:: python

  >>> from verboselib.heplers import to_language
  >>> to_language('en_US')
  'en-us'

Managing translation catalogs
-----------------------------

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

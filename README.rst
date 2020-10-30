verboselib
==========

A library with CLI tools allowing to add i18n and l10n to Python apps and libs with ease.

|pypi_package| |python_versions| |license|

|unix_build| |windows_build| |codebeat| |codacy| |scrutinizer|


**Contents**

.. contents::
  :local:
  :depth: 3
  :backlinks: none


Synopsis
--------

``verboselib`` is a thin abstraction layer on top of `GNU gettext`_ toolset and `Python gettext`_ module.

In contrast to the raw ``gettext`` API, ``verboselib`` provides a unified and thread-safe way to access translation catalogs and an easier way to set active language dynamically.

Additionally, it allows definitions of lazy translations, which can be useful for module-level variables or class-level attributes.

Besides, ``verboselib`` comes with a bunch of CLI tools for extracting translatable messages from sources and compiling them. Those tools do not impose code dependencies and can be used as stand-alone utilities.


Domains of Use
--------------

The primary domain of use is applications & services. However, it can also be used in libraries.

In such case users of a target library will have to be aware of using ``verboselib`` as well. Hence, ``verboselib`` can be viewed as an i18n & l10n framework.

Generally, reliance on frameworks is a thing to refrain from in stand-alone public libraries, but it can also be a totally valid design decision for auxiliary libraries at a product-level scale.


Installation
------------

Available as a `PyPI <https://pypi.python.org/pypi/verboselib>`_ package:

.. code-block:: bash

  pip install verboselib


Quickstart
----------

The following examples provide a quick overview of what usage of ``verboselib`` looks like.


Brief Example
~~~~~~~~~~~~~

The briefest usage example shows how to get immediate translations:

.. code-block:: python

  from verboselib import Translations  # (1)
  from verboselib import set_language  # (2)

  translations = Translations(         # (3)
    domain="the_app",
    locale_dir_path="locale",
  )
  _ = translations.gettext             # (4)

  set_language("en")                   # (5)
  print(_("Hi there!"))                # (6) 'Hi there!'

  set_language("sv")                   # (7)
  print(_("Hi there!"))                # (8) 'Hej där!'


And here is the explanation for the noted lines:

#. Import ``Translations`` class, which is a translations registry.
#. Import ``set_language()`` function, which allows switching between languages.
#. Create an instance of ``Translations`` class, specifying the messages domain and location of the translations catalogs directory.
#. Define ``_`` as a shortcut for ``translations.gettext()`` function.
#. Set the current language to English.
#. Print a ``Hi there!`` there message passed as an argument to the ``_`` function. This gives ``Hi there!`` as the output.
#. Set the current language to Swedish.
#. Print the same message again and get ``Hej där!`` as the output.


The example is naïve, but calls to ``gettext()`` via the ``_`` shortcut are very common inside functions, where messages are translated when functions are called. For example:

.. code-block:: python

  def print_message():
    print(_("Hi there!"))

  set_language("en")
  print_message()          # 'Hi there!'

  set_language("sv")
  print(_("Hi there!"))    # 'Hej där!'


Lazy Translations Example
~~~~~~~~~~~~~~~~~~~~~~~~~

Oftentimes there's a need to have a placeholder or just a message, the definition of which must be separated from its evaluation. This is achieved via lazy translations:

.. code-block:: python

  from verboselib import Translations
  from verboselib import set_language

  translations = Translations(
    domain="the_app",
    locale_dir_path="locale",
  )
  L_ = translations.gettext_lazy            # (1)

  class Greeter:
    greeting_fmt = L_("Hi there, {name}!")  # (2)

    @classmethod
    def make_greeting(cls, name):
      return cls.greeting_fmt.format(       # (3)
        name=name,
      )

  set_language("en")
  print(Greeter.make_greeting("user"))      # (4) 'Hi there, user!'

  set_language("sv")
  print(Greeter.make_greeting("user"))      # 'Hej där, user!'


Comments for the noted lines:

#. ``gettext_lazy`` is used instead of ``gettext`` and ``L_`` shortcut is used instead of ``_``.
#. A translatable string is defined as a class-level attribute using ``L_`` shortcut.
#. The translatable string is accessed as a normal string.
#. The method is called and a parameterized translated string is returned.


This example is also naïve, but here the value of ``Greeter.greeting_fmt`` is not translated into a solid string during construction of the ``Greeter`` class. This is important, as the class is constructed only once. The actual type of ``greeting_fmt`` is not a string, but ``verboselib.lazy.LazyString``, which is a string's proxy:

.. code-block:: python

  type(Greeter.greeting_fmt)
  # <class 'verboselib.lazy.LazyString'>


API
---

There are several aspects to consider when using ``verboselib``:

#. Active language.
#. Translations catalogs registry — an instance of ``verboselib.Translations`` class.
#. Translations catalogs directory — a directory where ``.po`` and ``.mo`` files are located.
#. Translatable messages themselves.
#. Tools for extracting messages and compiling translations.


The sections below describe those aspects separately.


Active Language
~~~~~~~~~~~~~~~

Active language is the language which will be used for getting final values of translatable strings.

Its **current value** is a string defined by a user, e.g. "en". The value can be missing, i.e. not set.

In addition to the current value, it is possible to define a **default value**. So, if the current value is not set, it will fallback to the default value.

By default, both "current value" and "default value" are not set, i.e. they are ``None``.

Finally, it's possible to **turn** translations **off**, so that translations will be equal to original messages.


Current Language
^^^^^^^^^^^^^^^^

The current language in ``verboselib`` is controlled and queried via the following functions:

``set_language(language)``
  Sets the current language for the current thread.

  .. code-block:: python

    from verboselib import set_language

    set_language("en")


``get_language()``
  Queries name of the current language in the current thread as a string.

  .. code-block:: python

    from verboselib import get_language
    from verboselib import set_language

    get_language()      # None

    set_language("en")
    get_language()      # 'en'


``drop_language()``
  Removes the value of the current language for the current thread. The value will fallback to the default value.

  .. code-block:: python

    from verboselib import drop_language
    from verboselib import get_language
    from verboselib import set_language

    set_language("en")
    get_language()      # 'en'

    drop_language()
    get_language()      # None


Default Language
^^^^^^^^^^^^^^^^

The default language is controlled by functions which are similar to functions used to control the current language:

``set_default_language(language)``
  Sets the default language for the current thread.

  .. code-block:: python

    from verboselib import set_default_language

    set_default_language("en")


``get_default_language``
  Queries value of the default language for the current thread as a string.

  .. code-block:: python

    from verboselib import get_default_language
    from verboselib import set_default_language

    get_default_language()      # None

    set_default_language("en")
    get_default_language()      # 'en'


``drop_default_language``
  Removes the value of the default language for the current thread.

  .. code-block:: python

    from verboselib import drop_default_language
    from verboselib import get_default_language
    from verboselib import set_default_language

    set_default_language("en")
    get_default_language()      # 'en'

    drop_default_language()
    get_default_language()      # None


Usually, only the ``set_default_language(...)`` is used. This can be helpful if ``None`` is a possible value for the current language. In such a case at least a default language will be used:

.. code-block:: python

  def greet_user(user):
    set_language(user.language)                           # can be None
    print(_("Hi there, {name}!").format(name=user.name))
    drop_language()

  set_default_language("en")
  ...
  user = get_user()
  greet_user(user)


Disabling Translations
^^^^^^^^^^^^^^^^^^^^^^

At certain times it can be useful to disable translations, for example, during debugging.

This can be done via ``set_language_bypass()`` function. It disables the current language and prevents it from falling back to the default language.

.. code-block:: python

  from verboselib import drop_language
  from verboselib import get_language
  from verboselib import set_language
  from verboselib import set_default_language
  from verboselib import set_language_bypass

  set_default_language("en")

  set_language("fr")
  get_language()              # 'fr'

  set_language_bypass()
  get_language()              # None

  drop_language()
  get_language()              # 'en'


Note that the 2nd call to ``get_language()`` returned ``None``.


Locale-to-language Conversions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``verboselib`` comes up with a couple of helper functions for converting languages to locales:

.. code-block:: python

  from verboselib import to_locale

  to_locale("en-us")                  # 'en_US'


and vice versa, for converting locales to languages:

.. code-block:: python

  from verboselib import to_language

  to_language("en_US")                # 'en-us'


Translations Catalogs Registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Translations catalogs registry (``verboselib.Translations``) is a facade in front of `gettext.GNUTranslations`_.


Instance Creation
^^^^^^^^^^^^^^^^^

The ``verboselib.Translations`` class requires the following arguments to be provided:

``domain``
  A name (``string``) of the domain of translations. Usually, it's the name of the application, of the library, or it can be just ``"messages"``.

``locale_dir_path``
  A path (``string`` or ``pathlib.Path``) to the translations catalogs directory, which is a place where actual translations are stored. Usually, such directory is called ``locale`` and is located inside the top-level directory of the application or library. The path is strongly recommended to be absolute.


Example:

.. code-block:: python

  from pathlib import Path

  from verboselib import Translations

  __here__ = Path(__file__).absolute().parent

  translations = Translations(
    domain="messages",
    locale_dir_path=(__here__ / "locale"),
  )


Instance Location
^^^^^^^^^^^^^^^^^

Although instances of ``Translations`` are just objects which can be passed to functions, it is recommended to create a single instance of ``Translations`` as a global variable in a separate module, say ``translations.py``. Those instances are thread-safe.

Additionally, it can be handy to make module-level aliases for the methods of a ``Translations`` instance:

.. code-block:: python

  # foo_package/translations.py

  from pathlib import Path

  from verboselib import Translations

  translations = Translations(
    domain="foo_package",
    locale_dir_path=(Path(__file__).absolute().parent / "locale"),
  )
  gettext = translations.gettext
  gettext_lazy = translations.gettext_lazy


This can look a bit ugly, but in such a case it's convenient to access those methods as functions from other modules, e.g.:

.. code-block:: python

  # foo_package/logic.py

  from .translations import gettext as _
  from .translations import gettext_lazy as L_

  print(_("Hello"))

  greeting_fmt = L_("Hello, {name}")


Methods
^^^^^^^

The API of ``verboselib.Translations`` is compatible with ``GNUTranslations`` and includes the following methods:

#. ``gettext(message)``
#. ``ngettext(singular, plural, n)``
#. ``pgettext(context, message)``
#. ``npgettext(context, singular, plural, n)``


Additionally, ``verboselib.Translations`` provides their lazy versions:

#. ``gettext_lazy(message)``
#. ``ngettext_lazy(singular, plural, n)``
#. ``pgettext_lazy(context, message)``
#. ``npgettext_lazy(context, singular, plural, n)``


Those lazy methods return an instance of ``verboselib.lazy.LazyString`` which is a string's proxy.

As for ``ngettext`` and ``npgettext`` methods and their lazy counterparts, not only an ``int`` can be passed as the ``n`` argument, but also a callable accepting no arguments and returning an ``int``. For example, both the following calls are valid and conceptually identical:

.. code-block:: python

  translations.ngettext("window", "windows", 1)
  translations.ngettext("window", "windows", lambda: 1)


Translations Catalogs Directory
-------------------------------

All translations are stored in a catalogs directory, where each language has its own subdirectory.

This section describes how to build such a catalog.


Workflow Overview
~~~~~~~~~~~~~~~~~

Firstly, translatable messages are extracted from source files into ``.po`` files. Those files contain IDs of messages and file locations where those messages are observed, e.g.:

.. code-block::

  #: foo.py:105 foo.py:203
  msgid "Hi there, {name}!"
  msgstr ""


Translators fill in, well, translations for IDs inside ``.po`` files:

.. code-block::

  #: foo.py:105 foo.py:203
  msgid "Hi there, {name}!"
  msgstr "Hej där, {name}!"


Finally, those ``.po`` files are compiled into ``.mo`` files.


Discovery of Translatable Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to be discovered and extracted, messages in source files have to be marked in a certain way.

This is achieved by wrapping a message by a pair of parentheses ``()`` prefixed by a `keyword`_. This makes it look like a function call, which it really is:

.. code-block:: python

  gettext("a message")


Here, ``gettext`` is used as a keyword. It's also possible to use its shortcut which is ``_``:

.. code-block:: python

  _("a message")


Both of those variants are equal, but the latter is more concise.

By default ``verboselib`` recognizes the following keywords:

================== ======== ===================================================
Keyword            Shortcut Example
================== ======== ===================================================
``gettext``        ``_``    ``_("message")``
``gettext_lazy``   ``L_``   ``L_("message")``
``ngettext``       ``N_``   ``N_("single", "plural", 123)``
``ngettext_lazy``  ``LN_``  ``LN_("single", "plural", 123)``
``pgettext``       ``P_``   ``P_("message context", "message")``
``pgettext_lazy``  ``LP_``  ``LP_("message context", "message")``
``npgettext``      ``NP_``  ``LP_("message context", "single", "plural", 123)``
``npgettext_lazy`` ``LNP_`` ``LP_("message context", "single", "plural", 123)``
================== ======== ===================================================


Technically, any literal can be used as a keyword. But if a non-default keyword is used, it must be specified during extraction, which is described later.


``.po`` files
~~~~~~~~~~~~~

Every ``.po`` file includes a header at the beginning.

It consists of key-value metadata separated from file's body via a blank line. Example:

.. code-block::

  msgid ""
  msgstr ""
  "Project-Id-Version: foo 1.0.0\n"
  "PO-Revision-Date: 2020-10-09 21:24+0300\n"
  "Report-Msgid-Bugs-To: support@foo.com\n"
  "Last-Translator: Mr Translator <translation-team@foo.com>\n"
  "Language: de\n"
  "MIME-Version: 1.0\n"
  "Content-Type: text/plain; charset=UTF-8\n"
  "Content-Transfer-Encoding: 8bit\n"

  msgid "Log in"
  msgstr ""


Refer to ``gettext`` docs for more details on `.po files <https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html>`_ and on `.po headers <https://www.gnu.org/software/gettext/manual/html_node/Header-Entry.html>`_.


Message Contexts
~~~~~~~~~~~~~~~~

Functions as ``pgettext()``, ``npgettext()``, and their lazy fellows allow to provide a message context.

This is just a string which will appear in ``.po`` files to give a hint for translators about the meaning of the message.

For example, the following call to ``pgettext``:

.. code-block:: python

  P_("abbrev. month", "Jan")


will add a ``msgctxt`` attribute into ``.po`` files:

.. code-block::

  #: foo.py:90
  msgctxt "abbrev. month"
  msgid "Jan"
  msgstr ""


Plural Forms
~~~~~~~~~~~~

Functions as ``ngettext()``, ``npgettext()``, and their lazy counterparts allow to get different translations depending on the integer number ``n`` provided to them, e.g.:

.. code-block:: python

  N_("window", "windows", 1)


In this trivial example ``n`` is ``1``. However, it can be a variable or a parameterless callable returning an ``int``:

.. code-block:: python

  def get_users_online() -> int:
    n = ...
    return n

  N_("user online", "users online", get_users_online)


This looks pretty simple, but that is not the end of the story.

Different languages can have different number of plural forms and each form can have their own calculation rules.

So, in order to make plural forms actually work, each ``.po`` file must include a ``Plural-Forms`` metadata in its header.

For example, languages of the Germanic family, like English, have 2 plural forms defined as:

.. code-block::

  "Plural-Forms: nplurals=2; plural=n != 1\n"


Examples of rules for other languages can be found at `Plural-Forms documentation page <https://www.gnu.org/software/gettext/manual/html_node/Plural-forms.html>`_.


Finally, every message having plural forms must have as many translations as there are plural forms specified by ``Plural-Forms``. For example:

.. code-block::

  #: foo.py:74
  msgid "window"
  msgid_plural "windows"
  msgstr[0] "вікно"
  msgstr[1] "вікна"
  msgstr[2] "вікон"

Refer to ``gettext`` docs for more info on `translating plural forms <https://www.gnu.org/software/gettext/manual/html_node/Translating-plural-forms.html>`_.


Utilities
---------

``verboselib`` comes with a couple of stand-alone CLI utilities for extracting and compiling translatable messages.

These utilities are implemented as subcommands of the main command named ``verboselib``.

Run ``verboselib`` with ``-h`` flag to get generic help:

.. code-block::

  verboselib -h

  usage: verboselib [-h] [-V] {extract,x,compile,c} ...

  run a verboselib command

  optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show version of verboselib and exit

  subcommands:
    {extract,x,compile,c}
      extract (x)         extract translatable strings from sources into '.po' files
      compile (c)         compile '.po' text files into '.mo' binaries


``extract`` or ``x``
~~~~~~~~~~~~~~~~~~~~

Used to extract translatable messages from sources. Creates or updates the directory with translations catalogs. Run with ``-h`` flag for help:

.. code-block::

  verboselib x -h

  usage: extract [-h] [-d DOMAIN] [-l LOCALE] [-a] [-o OUTPUT_DIR] [-k KEYWORD] [--no-default-keywords] [-e EXTENSIONS] [-s] [-i PATTERN] [--no-default-ignore] [--no-wrap]
                [--no-location] [--no-obsolete] [--keep-pot] [--xgettext-extra-args XGETTEXT_EXTRA_ARGS] [--msguniq-extra-args MSGUNIQ_EXTRA_ARGS]
                [--msgmerge-extra-args MSGMERGE_EXTRA_ARGS] [--msgattrib-extra-args MSGATTRIB_EXTRA_ARGS] [-v]

  extract translatable strings from sources into '.po' files

  optional arguments:
    -h, --help            show this help message and exit
    -d DOMAIN, --domain DOMAIN
                          domain of message files (default: messages)
    -l LOCALE, --locale LOCALE
                          create or update '.po' message files for the given locale(s), ex: 'en_US'; can be specified multiple times (default: None)
    -a, --all             update all '.po' message files for all existing locales (default: False)
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                          path to the directory where locales will be stored, a.k.a. 'locale dir' (default: locale)
    -k KEYWORD, --keyword KEYWORD
                          extra keyword to look for, ex: 'L_'; can be specified multiple times (default: None)
    --no-default-keywords
                          do not use default keywords as {'_', 'gettext', 'L_', 'gettext_lazy', 'N_:1,2', 'ngettext:1,2', 'LN_:1,2', 'ngettext_lazy:1,2', 'P_:1c,2',
                          'pgettext:1c,2', 'LP_:1c,2', 'pgettext_lazy:1c,2', 'NP_:1c,2,3', 'npgettext:1c,2,3', 'LNP_:1c,2,3', 'npgettext_lazy:1c,2,3'} (default: False)
    -e EXTENSIONS, --extension EXTENSIONS
                          extra file extension(s) to scan in addition to '.py'; separate multiple values with commas or specify the parameter multiple times (default: None)
    -s, --links           follow links to files and directories when scanning sources for translation strings (default: False)
    -i PATTERN, --ignore PATTERN
                          extra glob-style patterns for ignoring files or directories; can be specified multiple times (default: None)
    --no-default-ignore   do not ignore the common glob-style patterns as {'.*', '*~', 'CVS', '__pycache__', '*.pyc'} (default: False)
    --no-wrap             do not break long message lines into several lines (default: False)
    --no-location         do not write location lines, ex: '#: filename:lineno' (default: False)
    --no-obsolete         remove obsolete message strings (default: False)
    --keep-pot            keep '.pot' file after creating '.po' files (useful for debugging) (default: False)
    --xgettext-extra-args XGETTEXT_EXTRA_ARGS
                          extra arguments for 'xgettext' utility; can be comma-separated or specified multiple times (default: None)
    --msguniq-extra-args MSGUNIQ_EXTRA_ARGS
                          extra arguments for 'msguniq' utility; can be comma-separated or specified multiple times (default: None)
    --msgmerge-extra-args MSGMERGE_EXTRA_ARGS
                          extra arguments for 'msgmerge' utility; can be comma-separated or specified multiple times (default: None)
    --msgattrib-extra-args MSGATTRIB_EXTRA_ARGS
                          extra arguments for 'msgattrib' utility; can be comma-separated or specified multiple times (default: None)
    -v, --verbose         use verbose output (default: False)


The basic usage example:

.. code-block:: bash

  verboselib x -l 'uk' -l 'en' -l 'it'


Use ``-a`` flag to update all existing ``.po`` files:

.. code-block:: bash

  verboselib x -a


Use ``--keyword`` (``-k``) argument to specify additional keywords to look for, e.g.:

.. code-block:: bash

  verboselib x -a -k 'FOO_' -k 'BAR_'


``compile`` or ``c``
~~~~~~~~~~~~~~~~~~~~

Compiles all ``.po`` files into ``.mo`` files. Basic usage has no arguments:

.. code-block:: bash

  verboselib c


Use ``-h`` flag for help:

.. code-block::

  verboselib c -h

  usage: compile [-h] [-d LOCALES_DIR] [-l LOCALE] [-e EXCLUDE] [-f] [--msgfmt-extra-args MSGFMT_EXTRA_ARGS] [-v]

  compile '.po' text files into '.mo' binaries

  optional arguments:
    -h, --help            show this help message and exit
    -d LOCALES_DIR, --locale-dir LOCALES_DIR
                          path to the directory where locales are stored (default: locale)
    -l LOCALE, --locale LOCALE
                          locale(s) to process, ex: 'en_US'; can be specified multiple times; all locales are processed if not specified (default: None)
    -e EXCLUDE, --exclude EXCLUDE
                          locale(s) to exclude, ex: 'en_US'; can be specified multiple times (default: None)
    -f, --use-fuzzy       use fuzzy translations (default: False)
    --msgfmt-extra-args MSGFMT_EXTRA_ARGS
                          extra arguments for 'msgfmt' utility; can be comma-separated or specified multiple times (default: None)
    -v, --verbose         use verbose output (default: False)


Thread-safety
-------------

The current and the default languages are `thread-local`_. Hence, the functions for manipulating and querying them, like ``set_language()``, are thread-safe. However, the values have to be set in each thread separately.

As for the translations catalog registry, ``verboselib.Translations``, it is also thread-safe, as it relies on `RLocks`__. It's recommended to be used in libraries. However, if the target is an application and it is guaranteed to be single-threaded, it's possible to use a not-thread-safe version:

.. code-block:: python

  from verboselib import NotThreadSafeTranslations


Changelog
---------

* `1.0.1`_ (Oct 30, 2020)

  * Fix ``verboselib.utils.export()`` helper which adds objects to ``__all__`` variable of their own modules.

* `1.0.0`_ (Oct 11, 2020)

  API changes:

  * ``verboselib.factory.TranslationsFactory`` is now ``verboselib.translations.Translations``.
  * ``locale_dir`` argument of ``Translations`` is ``locale_dir_path`` now and instances of ``pathlib.Path`` can be used in addition to strings.
  * ``verboselib.translations.Translations`` is now thread-safe.
  * ``verboselib.translations.NotThreadSafeTranslations`` is added.
  * Methods ``ugettext()`` and ``ugettext_lazy()`` are removed from ``Translations``.
  * Methods ``ngettext()``, ``ngettext_lazy()``, ``pgettext()``, ``pgettext_lazy()``, ``npgettext()``, and ``npgettext_lazy()`` are added to ``Translations``.
  * Function ``get_default_language()`` is added.
  * Function ``verboselib.heplers.to_locale()`` no longer has ``to_lower`` argument.
  * ``verboselib-manage`` CLI utility is now just ``verboselib``.
  * ``compile`` and ``extract`` subcommands of ``verboselib`` have ``c`` and ``x`` aliases respectively.
  * Flags ``--no-default-keywords``, ``--xgettext-extra-args``, ``--msguniq-extra-args``, ``--msgmerge-extra-args``, and ``--msgattrib-extra-args`` are added to the ``extract`` command.
  * Flags ``--exclude``, ``--use-fuzzy``, and ``--msgfmt-extra-args`` are added to the ``compile`` command.

  Python support:

  * Support of all ``Python`` versions below ``3.7`` is dropped.

  Other:

  * All external dependencies are removed.
  * The license is switched from ``LGPLv3`` to ``MIT``.


* `0.2.1`_ (Jul 16, 2017)

  * Fix ``version`` command.
  * Rename ``verboselib-manage.py`` executable to simply ``verboselib-manage``.


* `0.2.0`_ (Dec 31, 2014)

  * Add ``get_default_language()`` method.
  * Use default translation classes from ``gettext`` module.


* `0.1.0`_ (Jul 17, 2014)

  Initial version.


.. |unix_build| image:: https://img.shields.io/travis/oblalex/verboselib
   :target: https://travis-ci.org/oblalex/verboselib

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/bdm3jnvuka1qjcm1/branch/master?svg=true
    :target: https://ci.appveyor.com/project/oblalex/verboselib
    :alt: Build status of the master branch on Windows

.. |codebeat| image:: https://codebeat.co/badges/6a606844-25df-4518-8e1f-3613907fcdb1
   :target: https://codebeat.co/projects/github-com-oblalex-verboselib-master
   :alt: Code quality provided by «Codebeat»

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/2e1b914f5ff741e2bf57605059f36485
   :target: https://www.codacy.com/gh/oblalex/verboselib/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=oblalex/verboselib&amp;utm_campaign=Badge_Grade
   :alt: Code quality provided by «Codacy»

.. |scrutinizer| image:: https://scrutinizer-ci.com/g/oblalex/verboselib/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/oblalex/verboselib/?branch=master
   :alt: Code quality provided by «Scrutinizer CI»

.. |pypi_package| image:: https://img.shields.io/pypi/v/verboselib
   :target: http://badge.fury.io/py/verboselib/
   :alt: Version of PyPI package

.. |python_versions| image:: https://img.shields.io/badge/Python-3.7,3.8-brightgreen.svg
   :alt: Supported versions of Python

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/oblalex/verboselib/blob/master/LICENSE
   :alt: MIT license


.. _GNU gettext: https://www.gnu.org/software/gettext/
.. _Python gettext: https://docs.python.org/3/library/gettext.html
.. _gettext.GNUTranslations: https://docs.python.org/3/library/gettext.html#the-gnutranslations-class
.. _keyword: https://www.gnu.org/software/gettext/manual/html_node/Mark-Keywords.html
.. _thread-local: https://docs.python.org/3/library/threading.html#thread-local-data

.. _rlock: https://docs.python.org/3/library/threading.html#rlock-objects
__ rlock_

.. _1.0.1: https://github.com/oblalex/verboselib/compare/v1.0.0...v1.0.1
.. _1.0.0: https://github.com/oblalex/verboselib/compare/v0.2.1...v1.0.0
.. _0.2.1: https://github.com/oblalex/verboselib/compare/v0.2.0...v0.2.1
.. _0.2.0: https://github.com/oblalex/verboselib/compare/v0.1.0...v0.2.0
.. _0.1.0: https://github.com/oblalex/verboselib/releases/tag/v0.1.0

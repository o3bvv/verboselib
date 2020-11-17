from ._utils import export


@export
def to_locale(language):
  """
  Turn a language name (en-us) into a locale name (en_US).

  Extracted `from Django <https://github.com/django/django/blob/e74b3d724e5ddfef96d1d66bd1c58e7aae26fc85/django/utils/translation/__init__.py#L274-L287>`_.

  """
  language, _, country = language.lower().partition("-")
  if not country:
    return language

  # A language with > 2 characters after the dash only has its first
  # character after the dash capitalized; e.g. sr-latn becomes sr_Latn.
  # A language with 2 characters after the dash has both characters
  # capitalized; e.g. en-us becomes en_US.
  country, _, tail = country.partition("-")
  country = country.title() if len(country) > 2 else country.upper()
  if tail:
    country += "-" + tail

  return language + "_" + country


@export
def to_language(locale):
  """
  Turn a locale name (en_US) into a language name (en-us).

  Extracted `from Django <https://github.com/django/django/blob/e74b3d724e5ddfef96d1d66bd1c58e7aae26fc85/django/utils/translation/__init__.py#L265-L271>`_.

  """
  p = locale.find("_")
  if p >= 0:
    return locale[:p].lower() + "-" + locale[p + 1:].lower()
  else:
    return locale.lower()

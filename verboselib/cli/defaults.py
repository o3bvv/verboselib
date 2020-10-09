DEFAULT_DOMAIN = "messages"

DEFAULT_LOCALE_DIR_NAME = "locale"

DEFAULT_IGNORE_PATTERNS = [
  ".*",
  "*~",
  "CVS",
  "__pycache__",
  "*.pyc",
]

DEFAULT_KEYWORDS = [
  "_",           "gettext",
  "L_",          "gettext_lazy",
  "N_:1,2",      "ngettext:1,2",
  "LN_:1,2",     "ngettext_lazy:1,2",
  "P_:1c,2",     "pgettext:1c,2",
  "LP_:1c,2",    "pgettext_lazy:1c,2",
  "NP_:1c,2,3",  "npgettext:1c,2,3",
  "LNP_:1c,2,3", "npgettext_lazy:1c,2,3",
]

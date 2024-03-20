import gettext
import locale
import os

from libtextworker.general import GetCurrentDir, test_import
from libtextworker.versioning import is_development_version_from_project, require

currdir = GetCurrentDir(__file__, True)
__version__ = "1.5a1"

require("libtextworker", "0.1.4b1")
test_import("tkinter")
test_import("pygubu")
test_import("cairosvg") # TODO

icon = currdir / "data" / "icons"

if is_development_version_from_project("texteditor"):
    icon /= "me.lebao3105.textworker.Devel.svg"
else:
    icon /= "me.lebao3105.textworker.svg"

LOCALE_DIR = currdir / "po"
VIEWS_DIR = currdir / "views"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")
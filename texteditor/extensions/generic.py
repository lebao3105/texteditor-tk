# For texteditor's local use only.
import logging
import os
import typing

from libtextworker.general import CraftItems, GetCurrentDir, Logger, strhdlr, formatter
from libtextworker.get_config import GetConfig
from libtextworker.interface.tk import ColorManager
from libtextworker.versioning import is_development_version_from_project

from libtextworker import EDITOR_DIR, THEMES_DIR, TOPLV_DIR

CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("texteditor") else ""
    )
)
DATA_PATH: str = CraftItems(GetCurrentDir(__file__), "..", "data")


clrcall: ColorManager
configs: str
global_settings: GetConfig
_editor_config_load: str
_theme_load: str


logger = Logger("texteditor", logging.INFO)
logger.UseGUIToolKit("tk")

filehdlr = logging.FileHandler(os.path.expanduser("~/.logs/texteditor.log"))
filehdlr.setFormatter(formatter)

logger.addHandler(strhdlr)
logger.addHandler(filehdlr)


def find_resource(t: typing.Literal["theme", "editor"]) -> str:
    if t == "theme":
        _name = global_settings["config-paths.ui"]["theme"]
        _path = global_settings["config-paths.ui"]["path"]

    else:
        _name = global_settings["config-paths.editor"]["name"]
        _path = global_settings["config-paths.editor"]["path"]

    _name += ".ini"

    if _path != "unchanged":
        _path = os.path.normpath(os.path.expanduser(_path))
    else:
        _path = THEMES_DIR if t == "theme" else EDITOR_DIR

    return CraftItems(_path, _name)


def ready():
    global _theme_load, _editor_config_load
    global clrcall, configs, global_settings
    global THEMES_DIR, EDITOR_DIR, TOPLV_DIR

    configs = open(CraftItems(DATA_PATH, "appconfig.ini"), "r").read()
    global_settings = GetConfig(configs, CONFIGS_PATH, True)

    logger.info(f"Settings path: {CONFIGS_PATH}")
    logger.info(f"Application datas (icon, updater, default settings) are stored in {DATA_PATH}")

    TOPLV_DIR = os.path.dirname(CONFIGS_PATH)
    THEMES_DIR = TOPLV_DIR + "/themes/"
    EDITOR_DIR = TOPLV_DIR + "/editorconfigs/"

    logger.info(f"Themes directory: {THEMES_DIR}")
    logger.info(f"Editor settings directory: {EDITOR_DIR}")

    _theme_load = find_resource("theme")
    _editor_config_load = find_resource("editor")

    clrcall = ColorManager(customfilepath=_theme_load)
    clrcall.recursive_configure = True

    logger.info("Ready to go!")
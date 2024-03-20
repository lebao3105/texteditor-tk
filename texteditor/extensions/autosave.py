from libtextworker.general import CraftItems
from pygubu.builder import Builder
from texteditor import VIEWS_DIR
from threading import Thread
from tkinter import Misc, Toplevel
from typing import Callable
from .generic import clrcall, global_settings

__all__ = ( "TOGGLE", "AutoSave", "AutoSaveConfig", "AUTOSV_DELAY" )

TOGGLE: bool = global_settings.getkey("editor.autosave", "enable", False, True) in global_settings.yes_values
AUTOSV_DELAY: int = global_settings.getkey("editor.autosave", "time", False, True)

if not int(AUTOSV_DELAY):
    AUTOSV_DELAY = 30

class AutoSave:
    Editor: Misc
    CurrDelay: int = AUTOSV_DELAY
    SaveFunc: Callable

    def Start(self, delay: int = AUTOSV_DELAY):
        if not TOGGLE: return
        self.CurrDelay = delay
        self.TaskId = self.Editor.after(int(delay) * 1000, lambda: self.SaveFunc())

    def Stop(self):
        self.Editor.after_cancel(self.TaskId)
        del self.TaskId

    def CheckToggle(self):
        if not TOGGLE and hasattr(self, "TaskId"):
            self.Stop()
        elif not hasattr(self, "TaskId"):
            self.Start()

    def Toggle(self, on: bool):
        if on:
            self.Start()
        else:
            self.Stop()

    def __init__(self):
        Thread(target=self.CheckToggle, daemon=True).start()


class AutoSaveConfig:
    """
    Autosave window.
    """

    timealiases = {
        _("30 seconds"): 30,
        _("1 minute"): 60,
        _("2 minutes"): 120,
        _("5 minutes"): 300,
        _("10 minutes"): 600,
        _("15 minutes"): 900,
        _("20 minutes"): 1200,
        _("30 minutes"): 1800
    }

    def ShowWind(self, master: Misc | None = None):
        """
        Shows the thing this class supposed to show.
        In older versions: this is placed under \__init__ method.
        But as this uses Toplevel which automatically shows itself (seems intended),
        the dialog creation has been moved here.
        """
        self.dialog = Toplevel(master)
        self.dialog.wm_title("AutoSave config")
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.builder = Builder(_)
        self.builder.add_from_file(CraftItems(VIEWS_DIR, "autosave.ui"))

        frame = self.builder.get_object("frame", self.dialog)
        self.combobox = self.builder.get_object("combobox1", frame)
        self.checkbtn = self.builder.get_object("checkbutton1", frame)
        self.combobox["values"] = list(self.timealiases)
        self.combobox["state"] = "readonly"

        clrcall.configure(frame, childs_too=True)
        clrcall.autocolor_run(frame)
        self.builder.connect_callbacks(self)

    def do_the_task(self):
        choice = self.builder.get_variable("selected_time").get()
        do_save = self.builder.get_variable("save").get()
        if choice:
            global_settings.set("editor.autosave", "time", self.timealiases[choice])
            if do_save:
                global_settings.update()

    def destroy(self):
        self.dialog.destroy()

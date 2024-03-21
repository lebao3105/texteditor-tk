import os
import pygubu
import texteditor
import webbrowser

from libtextworker.general import ResetEveryConfig, Importable
from libtextworker.interface.tk.dirctrl import DirCtrl, DC_HIDEROOT
from libtextworker.interface.tk.findreplace import *

from tkinter.filedialog import askdirectory
from tkinter import Menu, PhotoImage, TclError, Tk, Toplevel
from tkinter import messagebox as msgbox
from typing import Literal, NoReturn

from .extensions.generic import CONFIGS_PATH, logger
from .extensions.generic import clrcall, global_settings
from .extensions import autosave
from .tabs import TabsViewer
from .views import about

CAIRO_AVAILABLE = Importable["cairosvg"]
if CAIRO_AVAILABLE: from cairosvg import svg2png # type: ignore

class MainWindow(Tk):

    def __init__(this, *args, **kwargs):
        Tk.__init__(this, *args, **kwargs)
        this.geometry("810x610")

        # Set the application icon
        if os.path.isfile(texteditor.icon) and CAIRO_AVAILABLE:
            svg2png(open(texteditor.icon, "r").read(), write_to="./icon.png")
            try:
                this.wm_iconphoto(False, PhotoImage(file="./icon.png"))
            except TclError as e:
                logger.warning("Unable to set application icon: ", e)

        # Build the UI
        this.builder = pygubu.Builder(_)
        this.builder.add_from_file(texteditor.VIEWS_DIR / "menubar.ui")

        this.notebook = TabsViewer(this, do_place=True)
        this.autosv = autosave.AutoSaveConfig()

        this.GetColor()
        this.LoadMenu()
        this.BindEvents()

        # BooleanVar_s
        this.wrapbtn = this.builder.get_variable("wrapbtn")
        this.autosave_local = this.builder.get_variable("autosave_local")
        this.autosave_global = this.builder.get_variable("autosave_global")

        if global_settings.getkey("editor.autosave", "enable") in global_settings.yes_values:
            this.autosave_global.set(True)
            this.autosave_local.set(True)
        
        # Colorize the app
        clrcall.configure(this)
        if clrcall.getkey("color", "auto", True, True, True):
            clrcall.autocolor_run(this) # Known issue: this.lb won't be updated on color change outside the app

    def LoadMenu(this):
        # Configure some required menu items callback
        this.callbacks = {
            "aboutdlg": lambda: about.About().ShowDialog(this),
            "add_tab": lambda: this.add_tab(),
            "autosv_local": lambda: this.autosv_config("local", "switch"),
            "autosv_global": lambda: this.autosv_config("global", "switch"),
            "autosv_localcfg": lambda: this.autosv_config("local"),
            "autosv_globalcfg": lambda: this.autosv_config("global"),
            "change_color": lambda: this.change_color(),
            "destroy": lambda: this.destroy(),
            "gofind": lambda: this.find(),
            "goreplace": lambda: this.replace(),
            "opencfg": lambda: this.opencfg(),
            "open_doc": lambda: webbrowser.open("https://lebao3105.gitbook.io/texteditor_doc"),
            "openfile": lambda: this.notebook.fileops.OpenFileDialog(),
            "openfolder": lambda: this.openfolder(),
            "savefile": lambda: this.notebook.fileops.SaveFileEvent(),
            "savefileas": lambda: this.notebook.fileops.SaveAs(),
            "resetcfg": lambda: this.resetcfg(),
            "toggle_wrap": lambda: this.toggle_wrap(),
        }

        menu = Menu(this)
        this.config(menu=menu)

        for menu_, name in [("menu1", _("File")), ("menu2", _("Edit")),
                            ("menu3", _("Config")), ("menu4", _("Help"))]:
            setattr(this, menu_, this.builder.get_object(menu_, this))
            menu.add_cascade(menu=getattr(this, menu_), label=name)

        this.builder.connect_callbacks(this.callbacks)

    def BindEvents(this):
        bindcfg = this.bind
        bindcfg("<Control-n>", this.add_tab)
        bindcfg("<Control-f>", lambda event: this.find())
        bindcfg("<Control-r>", lambda event: this.replace())
        bindcfg("<Control-Shift-S>", this.notebook.fileops.SaveAs)
        bindcfg("<Control-s>", this.notebook.fileops.SaveFileEvent)
        bindcfg("<Control-o>", this.notebook.fileops.OpenFileDialog)
        bindcfg("<Control-w>", this.notebook.fileops.GetEditorFromCurrTab().wrapmode)

    # Menu bar callbacks
    def resetcfg(this, event=None) -> NoReturn:
        if msgbox.askyesno(_("Warning"),
                           _("This will reset ALL configurations you have ever made. Continue?")):
            ResetEveryConfig()

    def opencfg(this, event=None):
        new = Toplevel(this)
        path = os.path.dirname(CONFIGS_PATH)
        new.wm_title(path)
        control = DirCtrl(new)
        control.SetFolder(path)
        control.Frame.pack(expand=True, fill="both")

    def GetColor(this):
        if clrcall.getkey("color", "background") == "dark":
            this.lb = "light"
        else:
            this.lb = "dark"

    def change_color(this, event=None):
        clrcall.configure(this, this.lb)
        clrcall.set("color", "background", this.lb)
        this.GetColor()

    def add_tab(this, event=None):
        return this.notebook.add_tab(idx="default")

    def toggle_wrap(this, event=None):
        toggle = this.wrapbtn.get()
        this.notebook.fileops.GetEditorFromCurrTab().configure(wrap="word" if toggle else "none")

    def autosv_config(this, type: Literal["global", "local"], type2: Literal["switch"] | None = None):
        if type == "global":
            if type2 == "switch":
                msgbox.showinfo(message=_("This is applied only for this session."))
                autosave.TOGGLE = this.autosave_global.get()
            else:
                this.autosv.ShowWind(this)
        else:
            if type2 == "switch":
                this.notebook.fileops.GetEditorFromCurrTab().Toggle(this.autosave_local.get())
            else:
                this.notebook.fileops.GetEditorFromCurrTab().ShowWind()

    def openfolder(this):
        path = askdirectory(initialdir=os.path.expanduser("~/"),
                            mustexist=True, parent=this, title=_("Open a directory"))
        new = Toplevel(this)
        control = DirCtrl(new)
        control.SetFolder(path)
        control.Frame.pack(expand=True, fill="both")
        new.wm_title(path)
    
    def find(this):
        dlg = Toplevel(this)
        dlg.wm_title(_("Find for a text..."))
        FindReplace(dlg, this.notebook.fileops.GetEditorFromCurrTab(), TK_USEPACK).pack()
    
    def replace(this):
        dlg = Toplevel(this)
        dlg.wm_title(_("Find and Replace"))
        FindReplace(dlg, this.notebook.fileops.GetEditorFromCurrTab(), TK_USEPACK, True)
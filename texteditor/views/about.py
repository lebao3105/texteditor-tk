import platform
import sys
from tkinter import Misc, TclVersion, TkVersion, Toplevel
from tkinter.ttk import Button, Frame, Label, Notebook

from libtextworker.interface.tk.about import AboutDialog
from libtextworker.interface.tk.editor import StyledTextControl

from libtextworker import __version__ as libver
from texteditor import __version__ as appver
from texteditor.extensions.generic import clrcall


class About(AboutDialog):
    ProjectName = "textworker"
    ProjectVersion = appver
    ProjectSite = "https://github.com/lebao3105/texteditor-tk"

    ProjectDescription = _(
        "A text editor in Python, with customizable and easy-to-use user interface.\n"
        "Read documents online: https://lebao3105.gitbook.io/texteditor_doc"
    )

    ProjectLicense = \
        "(C) 2022-2024 Le Bao Nguyen.\n" \
        "This project is licensed under the GNU General Public License Version 3.0."

    ProjectBuilds: str = \
        f"""
        Libtextworker {libver}
        Tk {TkVersion}
        Tcl {TclVersion}
        Operating system: {platform.system()} version {platform.version()}
        Python {sys.version}"
        """

    Developers = "Le Bao Nguyen (@lebao3105)"
    Translators = Testers = Developers  # Looks sad

    def ShowDialog(self, master: Misc | None = None):
        dlg = Toplevel(master)
        dlg.wm_title(_("About this project"))
        dlg.grab_set()
        dlg.geometry("400x585")

        project_infos = _(
            "About this project\n"
            f"{self.ProjectName} version {self.ProjectVersion}\n"
            f"Description: {self.ProjectDescription}\n"
            f"Project website: {self.ProjectSite}"
        )

        project_credits = _(
            "This software is made possible by:\n" f"Developers:\n\t{self.Developers}"
        )

        if self.ArtMakers:
            project_credits += _(f"\nArtists:\n\t{self.ArtMakers}")

        if self.Testers:
            project_credits += _(f"\nTesters:\n\t{self.Testers}")

        if self.Translators:
            project_credits += _(f"\nTranslators:\n\t{self.Translators}")

        nb = Notebook(dlg)
        nb.pack(fill="both", expand=True)

        # Make tabs
        credits_te = StyledTextControl(dlg, wrap="word")
        license_te = StyledTextControl(dlg, wrap="word")
        license_te.insert(1.0, self.ProjectLicense)
        credits_te.insert(1.0, project_credits)
        license_te.configure(state="disabled")
        credits_te.configure(state="disabled")
        license_te.pack(expand=True, fill="both", anchor="nw")
        credits_te.pack(expand=True, fill="both", anchor="nw")

        nb.add(Label(dlg, text=project_infos, anchor="nw"), text=_("This software"))
        nb.add(credits_te._frame, text=_("Contributors"))
        nb.add(license_te._frame, text=_("License"))
        nb.add(Label(dlg, text=self.ProjectBuilds, anchor="nw"), text=_("System specifications"))

        # The bottom bar
        bottomfm = Frame(dlg)
        quitbtn = Button(bottomfm, text="OK", default="active")
        quitbtn.bind("<Button-1>", lambda evt: (dlg.destroy()))
        quitbtn.pack(side="right")
        bottomfm.pack(fill="x", side="bottom")

        clrcall.configure(dlg, childs_too=True)

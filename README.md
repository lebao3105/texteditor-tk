<div style="float: left;">
    <img src="https://raw.githubusercontent.com/lebao3105/texteditor/data/icons/me.lebao3105.textworker.svg">
    <img src="https://raw.githubusercontent.com/lebao3105/texteditor/data/icons/me.lebao3105.textworker.Devel.svg">
</div>

<p align="right">
    <h1 align="right">
        <strong>Textworker (Tkinter)</strong>
    </h1>
    <h3 align="right">
    A simple and cross-platform Python text editor.
    </h3>
    <a href="https://github.com/lebao3105/texteditor-tk/actions/workflows/wheeltk.yml">
        <image src="https://github.com/lebao3105/texteditor-tk/actions/workflows/wheeltk.yml/badge.svg?branch=data" align="right"/>
    </a>
</p>

Expected new features:

* About window ~~(but the contents seem not to be shown - wthell??)~~

* New auto-save implementation like the wip/wx branch - but it auto show on editor init (#1)

* New Find & Replace dialog - not usable right now

* An Editor class which embeds auto-save support by default

* Update libtextworker to 0.1.4 with fixes and new features

* Directory tree

These features will not here (comparing with wx builds):

* Markdown preview

* Preferences & Updater dialogs

## Features

* Lightweight

* Run some tasks with Command Window (removed on version 1.5a0)

* Customizable interface

* Auto save

* Multiple languages

See all app releases [here.](https://github.com/lebao3105/texteditor-tk/releases)

You can get wheels from [GitHub actions](https://github.com/lebao3105/texteditor-tk/actions).

## Build and install

Requires Python 3.10+ with Tkinter and pip installed.

Installable directly from TestPypi as the ```texteditor``` package.

To generate translations, which are not provided by default in the source code: Install gettext and make, then run:

```bash
make maketrans
```

Run the program:

```bash
python3 -m texteditor [args]
```

If you want to use the source code:

```bash
$ # install libtextworker[configparser, tkinter] first.
$ # install libtextworker[autocolor] for autocolor support.
$ git clone https://github.com/lebao3105/texteditor.git # Or you can use gitlab instead
$ cd texteditor
$ git submodule update --init --recursive
$ pip install cairosvg # If you want, for app icon support
```

Install from source: ```pip install -e .```

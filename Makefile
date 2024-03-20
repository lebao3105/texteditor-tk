# Used for maintaining tasks.
# Copyright (C) 2024 Le Bao Nguyen and contributors.
# Pround to be written in nano!

# Programs to use
GT = xgettext
MSF = msgfmt
MSM = msgmerge

# Project infomations
LOCALES = vi # Language codes, separated using spaces
POFILES = # Make later

# Targets
.PHONY: all maketrans makepot genmo $(LOCALES) build install

all: clean build

## Generate translations
maketrans: makepot genmo

makepot:
	@echo "[Translations] Making templates..."
	$(GT) --language=python -f po/POTFILES -d me.lebao3105.texteditor -o po/me.lebao3105.texteditor.pot

genmo: $(LOCALES)
$(LOCALES):
	@echo "[Translations] Making po for $@..."
	$(MSM) po/$@.po po/me.lebao3105.texteditor.pot -o po/$@.po

	@echo "[Translations] Compiling po for $@..."

	if [ ! -d po/$@ ]; then \
		mkdir po/$@; \
	fi

	if [ ! -d po/$@/LC_MESSAGE ]; then \
		mkdir po/$@/LC_MESSAGE; \
	fi
	$(MSF) po/$@.po -o po/$@/LC_MESSAGE/$@.mo

## Install
install: maketrans
	$(pip) install .

## Build
build: maketrans
	$(pip) install build
	$(python3) -m build .

## Clean
clean: $(wildcard po/*/LC_MESSAGES)
	rm -rf $?
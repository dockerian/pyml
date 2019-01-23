# Makefile at project top directory level

PROJECT ?= ml

USE_PYTHON3 := true
PYVENV_MAKE := ../tools/make_venv.sh
PYVENV_NAME ?= .venv


.PHONY: clean cover dev-setup show test
clean cover dev-setup show test:
	@echo
	cd .. && make $@

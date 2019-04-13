# Makefile for classifier

PROJECT ?= classifier

USE_PYTHON3 := true
PYVENV_MAKE := ../../tools/make_venv.sh
PYVENV_NAME ?= .venv


.PHONY: clean cover dev-setup show test
clean cover dev-setup show test:
	@echo
	cd .. && make $@



############################################################
# classifier targets
############################################################
.PHONY: predict prediction pr
predict prediction pr:
	@echo
ifneq ("$(VIRTUAL_ENV)", "")
	PYTHONPATH=../.. python prediction.py
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(PYVENV_MAKE) "$@"
endif
	@echo
	@echo "- DONE: $@"

.PHONY: training tr
training tr:
	@echo
ifneq ("$(VIRTUAL_ENV)", "")
	PYTHONPATH=../.. python training.py
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(PYVENV_MAKE) "$@"
endif
	@echo
	@echo "- DONE: $@"

# Makefile for digit_recognizer

PROJECT ?= digit_recognizer

USE_PYTHON3 := true
PYVENV_MAKE := ../../tools/make_venv.sh
PYVENV_NAME ?= .venv


.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


.PHONY: clean cover dev-setup show test
clean cover dev-setup show test:
	@echo
	cd .. && make $@



############################################################
# digit_recognizer targets
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

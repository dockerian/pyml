# Makefile at project top directory level

PROJECT ?= ml

USE_PYTHON3 := true
PYVENV_MAKE := ../tools/make_venv.sh
PYVENV_NAME ?= .venv

SHOW_IMAGE ?= true


# Don't need to start docker in 2 situations:
ifneq ("$(DOCKER_DENV)", "")  # assume inside docker container
	DONT_RUN_DOCKER := true
	SHOW_IMAGE := false
endif

ifneq ("$(VIRTUAL_ENV)", "")  # assume python venv is activated
	DONT_RUN_PYVENV := true
endif


.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs


.PHONY: clean cover dev-setup show test
clean cover dev-setup show test:
	@echo
	cd .. && make $@

.PHONY: cl classifier cl-training dr digit-recognizer dr-training
cl classifier cl-training dr digit-recognizer dr-training:
	@echo
	cd .. && make $@

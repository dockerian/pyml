# Makefile at project top directory level

PROJECT ?= ml

USE_PYTHON3 := true
PYVENV_MAKE := ../tools/make_venv.sh
PYVENV_NAME ?= .venv


.PHONY: clean cover dev-setup show test
clean cover dev-setup show test:
	@echo
	cd .. && make $@


############################################################
# sub-projects Makefile redirection
############################################################
.PHONY: classifier-prediction cpr
classifier-prediction cpr:
	@echo
	cd classifier && make prediction

.PHONY: classifier-training ctr
classifier-training ctr:
	@echo
	cd classifier && make training

.PHONY: digit-prediction dpr
digit-prediction dpr:
	@echo
	cd digit_recognizer && make prediction

.PHONY: digit-training dtr
digit-training dtr:
	@echo
	cd digit_recognizer && make training

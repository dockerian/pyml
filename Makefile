# Makefile at repository root
#
# Dependencies:
#   * Python 2.7 virtualenv or Python 3 venv module
#   * setup.py, setup.cfg, .pylintrc
#   * tools/make_venv.sh
#   * docker and tools/run.sh (to build docker image and run in container)
#   * $(PROJECT)/requirements-dev.txt (for dev and testing)
#   * $(PROJECT)/requirements.txt (for production)
#   * $(SYSTOOLS)
#
.PHONY: clean clean-cache

# Project name at top level of the repository
PROJECT := ml

############################################################
# Makefile variables and functions
############################################################
DOCKER_PORT ?= 8081
DOCKER_USER := dockerian
DOCKER_NAME := pyml
GITHUB_REPO := pyml
DOCKER_IMAG := $(DOCKER_USER)/$(DOCKER_NAME)
DOCKER_TAGS := $(shell docker images 2>&1|grep -m1 ${DOCKER_IMAG}|awk '{print $$1;}')
DOCKER_DENV := $(wildcard /.dockerenv)
DOCKER_PATH := $(shell which docker)
DOCKER_FILE ?= Dockerfile

BUILD_ENV ?= test
COVERAGE_DIR := htmlcov
COVERAGE_REPORT := $(COVERAGE_DIR)/index.html

SYSTOOLS := find rm python tee xargs zip

USE_PYTHON3 := true
PIPLIST_ALL := $(PROJECT)/requirements.txt
PIPLIST_DEV := $(PROJECT)/requirements-dev.txt
PY_LIB_PATH := $(shell python -c "import site; print(site.getsitepackages()[0])" 2>/dev/null)
PYTEST_ARGS := --flakes --pep8 --pylint -s -vv --cov-report term-missing
NOSE_2_ARGS := --output-buffer -v --with-coverage --coverage $(PROJECT) --coverage-report html --coverage-report term
UTTEST_ARGS := --buffer --catch --failfast --verbose
# Python venv (virtual env) directory name (without full path)
PYVENV_NAME ?= .venv

MAKE_BUILD := tools/build.sh
MAKE_VENV := tools/make_venv.sh
MAKE_RUN := tools/run.sh

# returns "" if all undefined; otherwise, there is defined.
ifdef_any_of = $(filter-out undefined,$(foreach v,$(1),$(origin $(v))))
# usage:
#   * checking if any defined
#     - ifneq ($(call ifdef_any_of,VAR1 VAR2),)
#   * checking if none defined
#     - ifeq ($(call ifdef_any_of,VAR1 VAR2),)

# returns "" if all defined; otherwise, there is undefined.
ifany_undef = $(filter undefined,$(foreach v,$(1),$(origin $(v))))
# usage:
#   * checking if any undefined
#     - ifneq ($(call ifany_undef,VAR1 VAR2),)
#   * checking if both defined
#     - ifeq ($(call ifany_undef,VAR1 VAR2),)

# Don't need to start docker in 2 situations:
ifneq ("$(DOCKER_DENV)", "")  # assume inside docker container
	DONT_RUN_DOCKER := true
endif
ifeq ("$(DOCKER_PATH)", "")   # docker command is NOT installed
	DONT_RUN_DOCKER := true
endif

# Don't need venv insider docker (in most situations)
ifneq ("$(DOCKER_DENV)", "")  # assume inside docker container
	DONT_RUN_PYVENV := true
endif
# Don't start venv (virtual env) if it is already activated:
ifneq ("$(VIRTUAL_ENV)", "")  # assume python venv is activated
	DONT_RUN_PYVENV := true
endif


############################################################
# Makefile targets
############################################################
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | \
	awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

.PHONY: check-tools
check-tools:
	@echo
	@echo "--- Checking for presence of required tools: $(SYSTOOLS)"
	$(foreach tool,$(SYSTOOLS),\
	$(if $(shell which $(tool)),$(echo "boo"),\
	$(error "ERROR: Cannot find '$(tool)' in system $$PATH")))
	@echo
	@echo "- DONE: $@"

clean clean-cache:
	@echo
	@echo "--- Removing pyc and log files"
	find . -name '.DS_Store' -type f -delete
	find . -name \*.pyc -type f -delete -o -name \*.log -delete
	find . -name '__pycache__' -type d -delete
	rm -Rf .cache
	rm -Rf .pytest_cache
	rm -Rf $(PROJECT)/.cache
	rm -rf log*.txt
	@echo
	@echo "--- Removing coverage files"
	find . -name '.coverage' -type f -delete
	find . -name '$(COVERAGE_DIR)' -type d | xargs rm -rf
	rm -rf cover
	rm -rf $(PROJECT)/cover
	rm -rf cover
	@echo
	@echo "--- Removing *.egg-info"
	rm -Rf *.egg-info
	rm -Rf $(PROJECT)/*.egg-info
	@echo
	@echo "--- Removing tox virtualenv"
	rm -Rf $(PROJECT)/.tox*
	rm -Rf .tox
	@echo
	@echo "--- Removing build"
	rm -rf $(PROJECT)_build.tee
	rm -rf build*
	@echo
	@echo "- DONE: $@"

clean-all: clean-cache
	@echo
ifeq ("$(DOCKER_DENV)", "")
	# not in a docker container
	@echo "--- Removing docker image $(DOCKER_TAGS)"
	docker rm -f $(shell docker ps -a|grep $(DOCKER_NAME)|awk '{print $$1}') 2>/dev/null || true
	docker rm -f $(shell docker ps -a|grep $(DOCKER_NAME)-prod|awk '{print $$1}') 2>/dev/null || true
	docker rmi -f $(shell docker images -a|grep $(DOCKER_TAGS) 2>&1|awk '{print $$1}') 2>/dev/null || true
	rm -rf docker_build.tee
endif
	@echo
ifneq ("$(VIRTUAL_ENV)", "")
	@echo "--- Cleaning up pip list in $(VIRTUAL_ENV) ..."
	python -m pip freeze | grep -v '^-e' | grep -v '^#' | grep -v 'pkg-resources' | xargs pip uninstall -y || true
	@echo ''
	@echo '**********************************************************************'
	@echo '* Please `deactivate` '"$(PYVENV_NAME) before cleaning all eggs and virtual env *"
	@echo '**********************************************************************'
else
	@echo "--- Removing virtual env"
	rm -rf *.tee
	rm -Rf $(PYVENV_NAME)
	rm -Rf .venv*
	rm -Rf .eggs
endif
	@echo
	@echo "- DONE: $@"


############################################################
# Makefile targets for venv (virtual env)
############################################################
$(PYVENV_NAME).tee: $(PIPLIST_DEV) $(PIPLIST_ALL)
	@make dev-setup-venv
	@echo
	@echo "- DONE: $(PYVENV_NAME)"

.PHONY: dev-setup-venv dev-setup
dev-setup-venv dev-setup: clean-cache check-tools
	@echo
ifneq ("$(VIRTUAL_ENV)", "")
	@echo "--- Cleaning up pip list in $(VIRTUAL_ENV) ..."
	python -m pip install --upgrade pip || true
	python -m pip freeze | grep -v '^-e' | grep -v '^#' | grep -v 'pkg-resources' | xargs pip uninstall -y || true
	@echo
	@echo "--- Setting up $(PROJECT) develop ..."
	# disabling setup.py due to easy_install issue on ubuntu
	# python setup.py develop
	@echo
	@echo "--- Installing required dev packages ..."
	# running setup.py in upper level of `$(PROJECT)` folder to register the package
	python -m pip install -r $(PIPLIST_ALL) | tee $(PYVENV_NAME).tee
	python -m pip install -r $(PIPLIST_DEV) | tee $(PYVENV_NAME).tee
	@echo
	python -m pip list
else
	@echo "Checking python venv: $(PYVENV_NAME)"
	@echo "----------------------------------------------------------------------"
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) "$@"
	# @touch $(PYVENV_NAME).tee
	@echo
endif
	@echo
	@echo "- DONE: $@"

.PHONY: setup test-setup
setup test-setup: $(PYVENV_NAME).tee
	@echo "----------------------------------------------------------------------"
	@echo "Python environment: $(PYVENV_NAME)"
	@echo "- Activate command: source $(PYVENV_NAME)/bin/activate"
	@echo

.PHONY: venv-clean dvenv
venv-clean dvenv:
	@echo
ifneq ("$(VIRTUAL_ENV)", "")
	@echo "----------------------------------------------------------------------"
	@echo "Python environment: $(VIRTUAL_ENV)"
	@echo "- Activate command: source $(VIRTUAL_ENV)/bin/activate"
	@echo "- Deactivating cmd: deactivate"
	@echo "----------------------------------------------------------------------"
else
	@echo "Cleaning up python venv: $(PYVENV_NAME)"
	rm -rf $(PYVENV_NAME)
	rm -Rf .eggs
endif
	@echo ""
	@echo "- DONE: $@"
	@echo ""

.PHONY: venv
venv: check-tools
	@echo
ifeq ("$(VIRTUAL_ENV)", "")
	@echo "Preparing for venv: [$(PYVENV_NAME)] ..."
	python3 -m venv $(PYVENV_NAME)
	@echo "----------------------------------------------------------------------"
	@echo "Python environment: $(PYVENV_NAME)"
	@echo "- Activate command: source $(PYVENV_NAME)/bin/activate"
else
	@echo "----------------------------------------------------------------------"
	@echo "- Activated python venv: $(VIRTUAL_ENV)"
endif
	@echo "----------------------------------------------------------------------"
	@echo "- DONE: $@"
	@echo ""


############################################################
# Makefile targets for docker
############################################################
docker cmd: docker_build.tee clean-cache
ifeq ("$(DOCKER_DENV)", "")
	@echo ""
	@echo `date +%Y-%m-%d:%H:%M:%S` "Start bash in container '$(DOCKER_NAME)'"
	PROJECT_DIR="$(PWD)" \
	GITHUB_USER=$(GITHUB_CORP) GITHUB_REPO=$(GITHUB_REPO) \
	DOCKER_USER=$(DOCKER_USER) DOCKER_NAME=$(DOCKER_NAME) \
	DOCKER_FILE=$(DOCKER_FILE) \
	$(MAKE_RUN) $@
else
	@echo "env in the container:"
	@echo "-----------------------------------------------------------------------"
	@env | sort
	@echo "-----------------------------------------------------------------------"
endif
	@echo "- DONE: $@"

docker_build.tee: $(DOCKER_FILE)
ifeq ("$(DOCKER_DENV)", "")
	# make in a docker host environment
	@echo ""
	@echo `date +%Y-%m-%d:%H:%M:%S` "Building '$(DOCKER_TAGS)'"
	@echo "-----------------------------------------------------------------------"
	docker build -f $(DOCKER_FILE) -t $(DOCKER_TAGS) . | tee docker_build.tee
	@echo "-----------------------------------------------------------------------"
	@echo ""
	docker images --all | grep -e 'REPOSITORY' -e '$(DOCKER_TAGS)'
	@echo "......................................................................."
	@echo "- DONE: {docker build}"
	@echo ""
endif


############################################################
# Makefile targets for testing
############################################################
.PHONY: coverage-only show
coverage-only show:
	@echo ""
ifeq ("$(DOCKER_DENV)", "")
	@echo "--- Opening $(COVERAGE_REPORT)"
ifeq ($(OS), Windows_NT) # Windows
	start "$(COVERAGE_REPORT)"
else ifeq ($(shell uname),Darwin) # Mac OS
	open "$(COVERAGE_REPORT)"
else
	nohup xdg-open "$(COVERAGE_REPORT)" >/dev/null 2>&1 &
endif
else
	@echo "- WARNING: Cannot open test coverage in the container."
endif

.PHONY: coverage cover
coverage cover: test coverage-only

functest: clean-cache check-tools
	@echo
ifeq ("$(DONT_RUN_PYVENV)", "true")
	@echo "--- Starting pytest for functional tests ..."
	@echo
	PYTHONPATH=. pytest -c setup.cfg -m "functest" $(PYTEST_ARGS) --cov-fail-under=20
	@echo
	@echo "- DONE: $@"
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) "$@"
endif

nosetest nosetests: clean-cache check-tools test-setup
	@echo
ifeq ("$(DONT_RUN_PYVENV)", "true")
	@echo "--- Starting nose2 tests ..."
	@echo
	PYTHONPATH=. nose2 $(NOSE_2_ARGS)
	@echo "......................................................................"
	@echo "See coverage report: $(COVERAGE_REPORT)"
	@echo
	@echo "- DONE: $@"
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) dev-setup "$@"
endif

python-test unittest: clean-cache check-tools test-setup
	@echo
ifeq ("$(DONT_RUN_PYVENV)", "true")
	@echo "--- Starting unittest discover ..."
	@echo
	# python -m unittest discover ${UTTEST_ARGS}
	PYTHONPATH=. python -m unittest discover -bcfv
	@echo
	@echo "- DONE: $@"
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) dev-setup "$@"
endif

pytest test: clean-cache check-tools test-setup test-only
	@echo
	@echo "- DONE: $@"

test-all: clean-all dev-setup-venv test-all-only
	@echo
	@echo "- DONE: $@"

test-all-only:
	@echo
ifeq ("$(DONT_RUN_PYVENV)", "true")
	# @echo "--- Setup $(PROJECT) develop [$@] ..."
	# python setup.py develop
	# @echo
	python -m pip list
	@echo
	@echo "--- Starting pytest for all tests ..."
	PYTHONPATH=. pytest -c setup.cfg $(PYTEST_ARGS)
	@echo
	@echo "- DONE: $@"
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) "$@"
endif

test-only:
	@echo
ifeq ("$(DONT_RUN_PYVENV)", "true")
	@echo "--- Python lib: $(PY_LIB_PATH)"
	@echo
	@echo "--- Starting pytest for unit tests ..."
	@echo
	PYTHONPATH=. pytest -c setup.cfg -m 'not functest' $(PYTEST_ARGS)
	@echo
	@echo "- DONE: $@"
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) "$@"
endif


############################################################
# build and deploy targets
############################################################
build: clean-cache build-only
build-only:
	@echo
	BUILD_ENV=$(BUILD_ENV) USE_PYTHON3=$(USE_PYTHON3) $(MAKE_BUILD)
	@echo
	@echo "- DONE: $@"

build-test: clean-cache build-test-only
build-test-only:
	@echo
	BUILD_ENV=test USE_PYTHON3=$(USE_PYTHON3) $(MAKE_BUILD)
	@echo
	@echo "- DONE: $@"


############################################################
# run
############################################################
API_CODE_FIRST := $(PROJECT).app_fastapi
API_SPEC_FIRST := $(PROJECT).app_connexion
API_APP_MODULE ?= $(PROJECT).app
API_APP_WSGI ?= gunicorn

run-api:
	@echo ""
ifndef DONT_RUN_DOCKER
	@echo "Starting $(DOCKER_TAGS)"
	@echo ""
	PROJECT_DIR="$(PWD)" \
	GITHUB_USER=$(GITHUB_CORP) GITHUB_REPO=$(GITHUB_REPO) \
	DOCKER_USER=$(DOCKER_USER) DOCKER_NAME=$(DOCKER_NAME) DOCKER_FILE="$(DOCKER_FILE)" \
	DOCKER_PORT=$(DOCKER_PORT) \
	$(MAKE_RUN) $@
else
ifeq ("$(DONT_RUN_PYVENV)", "true")
	env|sort
	@echo ""
	ENV=$(BUILD_ENV) \
	PYTHONPATH=. gunicorn --config=$(PROJECT)/config_$(API_APP_WSGI).py $(API_APP_MODULE):app
else
	USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(MAKE_VENV) "$@"
endif
endif
	@echo ""
	@echo "- DONE: $@"

run-gunicorn:
	@echo ""
	@echo "Starting API server with gunicorn wsgi"
	# --- requiring venv or docker
	# pip install gunicorn
	ENV=$(BUILD_ENV) \
	PYTHONPATH=. gunicorn --config=$(PROJECT)/config_gunicorn.py $(API_SPEC_FIRST):app
	@echo ""
	@echo "- DONE: $@"

run-gevent:
	@echo ""
	@echo "Starting API server with gevent wsgi"
	# --- requiring venv or docker
	# pip install gevent
	ENV=$(BUILD_ENV) \
	PYTHONPATH=. python3 $(PROJECT)/run_gevent.py
	@echo ""
	@echo "- DONE: $@"

run-fastapi:
	@echo ""
	@echo "Starting a fastapi server with gunicorn/uvicorn wsgi"
	# --- requiring venv or docker
	# pip install fastapi gunicorn uvicorn
	ENV=$(BUILD_ENV) \
	PYTHONPATH=. gunicorn --config=$(PROJECT)/config_uvicorn.py $(API_CODE_FIRST):app
	@echo ""
	@echo "- DONE: $@"

run-flask:
	@echo ""
	@echo "Starting a connexion/flask API server in dev mode"
	# --- requiring venv or docker
	# pip install flask connexion[all]
	ENV=$(BUILD_ENV) \
	PYTHONPATH=. python3 $(PROJECT)/app_connexion.py
	@echo ""
	@echo "- DONE: $@"

run-nginx-clean:
ifeq ("$(DOCKER_DENV)", "")
	@echo ""
	@echo "Cleaning $(DOCKER_NAME)-prod"
	docker rm -f $(shell docker ps -a|grep $(DOCKER_NAME)-prod|awk '{print $$1}') 2>/dev/null || true
	@echo ""
	docker ps -a
endif

run-nginx-build:
ifeq ("$(DOCKER_DENV)", "")
	@echo ""
	@echo "Building $(DOCKER_TAGS):prod"
	docker images -a| grep -e '$(DOCKER_TAGS) *prod' || \
	docker build -t $(DOCKER_TAGS):prod -f $(DOCKER_FILE).prod .
	@echo ""
	docker images -a| grep $(DOCKER_TAGS) 2>/dev/null
endif

run-nginx: run-nginx-clean run-nginx-build
	@echo ""
ifeq ("$(DOCKER_DENV)", "")
	@echo "Starting $(DOCKER_TAGS):prod"
	@echo ""
	PROJECT="$(PROJECT)" \
	PROJECT_DIR="$(PWD)" \
	DOCKER_PORT="$(DOCKER_PORT)" \
	ENV=$(BUILD_ENV) \
	docker run -d \
	-e ENV \
	--hostname $(DOCKER_NAME) --name $(DOCKER_NAME)-prod \
	-v $(PWD)/tools/nginx.conf:/etc/nginx/conf.d/default.conf \
	-v $(PWD):/src/$(GITHUB_REPO) \
	-p $(DOCKER_PORT):80 $(DOCKER_TAGS):prod \
	/bin/bash -c "make $@"
	@echo ""
	@echo "$(DOCKER_NAME)-prod is available at http://localhost:$(DOCKER_PORT)"
else
	env|sort
	@echo ""
	@which nginx || echo "Cannot find in $(DOCKER_NAME)-prod"
	nginx -g "pid $(PWD)/nginx.pid;"
	@echo ""
	PYTHONPATH=. gunicorn --config=$(PROJECT)/config_$(API_APP_WSGI).py $(API_APP_MODULE):app
endif
	@echo ""
	@echo "- DONE: $@"


############################################################
# swagger and api spec
############################################################
SWAGGER_PORT ?= 8881
SWAGGER_PAGE := http://localhost:$(SWAGGER_PORT)
SWAGGER_EDIT := swaggerapi/swagger-editor
SWAGGER_UIMG := swaggerapi/swagger-ui
# docker image for swagger web
SWAGGER_WTAG := $(DOCKER_NAME)-swagger
SWAGGER_NGNX := /usr/share/nginx
SWAGGER_SEDS := 'sed -i "s|cp -s \$$SWAGGER_JSON \$$NGINX_ROOT|\# cp -s \$$SWAGGER_JSON \$$NGINX_ROOT|g" /usr/share/nginx/docker-run.sh && . /usr/share/nginx/docker-run.sh'

SWAGGER_FILE := swagger.yaml
SWAGGER_PATH := $(PWD)/ml/apidoc/v1

swagger-clean:
	@echo ""
	@echo "Cleaning docker container: $(SWAGGER_WTAG)"
	@echo ""
	docker rm -f $(shell docker ps -a|grep $(SWAGGER_WTAG)|awk '{print $$1}') 2>/dev/null || true
	@echo ""
	@echo "- DONE: $@"

swagger swagger-ui: swagger-clean
	@echo ""
ifneq ("$(DOCKER_PATH)","")
	@echo "Starting $@ in docker container ..."
	docker run \
	--name $(SWAGGER_WTAG) \
	-d -p $(SWAGGER_PORT):8080 \
	-e SWAGGER_JSON=/tmp/$(SWAGGER_FILE) \
	-v $(SWAGGER_PATH):/tmp \
	$(SWAGGER_UIMG)
	@echo ""
ifeq ($(OS), Windows_NT) # Windows
	start $(SWAGGER_PAGE)
else ifeq ($(shell uname),Darwin) # Mac OS
	open $(SWAGGER_PAGE)
else
	nohup xdg-open $(SWAGGER_PAGE) >/dev/null 2>&1 &
endif
else
	@echo "Cannot start docker run for $@"
endif
	@echo ""
	@echo "- DONE: $@"

swagger-editor: swagger-clean
	@echo ""
ifneq ("$(DOCKER_PATH)","")
	@echo "Starting $@ in docker container ..."
	docker run \
	--name $(SWAGGER_WTAG) \
	-d -p $(SWAGGER_PORT):8080 \
	-e SWAGGER_JSON=$(SWAGGER_NGNX)/html/swagger.json \
	-v $(SWAGGER_PATH)/$(SWAGGER_FILE):$(SWAGGER_NGNX)/html/swagger.json \
	$(SWAGGER_EDIT)
	@echo ""
ifeq ($(OS), Windows_NT) # Windows
	start $(SWAGGER_PAGE)
else ifeq ($(shell uname),Darwin) # Mac OS
	open $(SWAGGER_PAGE)
else
	nohup xdg-open $(SWAGGER_PAGE) >/dev/null 2>&1 &
endif
	@echo "......................................................................."
	@echo "Started $@ at http"
else
	@echo "Cannot start docker run for $@"
endif
	@echo ""
	@echo "- DONE: $@"


############################################################
# sub-projects Makefile redirection
############################################################

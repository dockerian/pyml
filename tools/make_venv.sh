#!/usr/bin/env bash
############################################################
# Run "make ${1:-test}" inside a python venv (virtual env)
#
# From: https://github.com/jasonzhuyx
# Note:
#     - Using env USE_PYTHON3 or USE_PYTHON2 to specify python runtime
#     - USE_PYTHON3 takes precedence over USE_PYTHON2 (as default)
#     - Makefile example
# ```
# PYVENV_MAKE := tools/make_venv.sh
# PYVENV_NAME ?= .venv
# USE_PYTHON3 ?= false
#
# ifneq ("$(VIRTUAL_ENV)", "")
#       PYTHONPATH=. python main.py
# else
#       USE_PYTHON3=$(USE_PYTHON3) VENV_NAME=$(PYVENV_NAME) $(PYVENV_MAKE) "$@"
# endif
# ```
############################################################
set +x
script_file="$( readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo ${BASH_SOURCE[0]} )"
script_name="${script_file##*/}"
script_base="$( cd "$( echo "${script_file%/*}/.." )" && pwd )"
script_path="$( cd "$( echo "${script_file%/*}" )" && pwd )"

PYTHON_EXEC="python"
PY_LIB_PATH="$(pip show pip | grep Location | awk '{print substr($0, index($0,$2))}')"
DEF_VERSION="$(python  --version 2>&1 | grep 'Python' | awk '{print $2}')"
PY2_VERSION="$(python2 --version 2>&1 | grep 'Python' | awk '{print $2}')"
PY3_VERSION="$(python3 --version 2>&1 | grep 'Python' | awk '{print $2}')"
USE_PYTHON2="${USE_PYTHON2:-false}"
USE_PYTHON3="${USE_PYTHON3:-true}"
CMD_PY_VENV="virtualenv"
PIP_COMMAND="pip"

# main function
function main() {
  VENV_NAME="${VENV_NAME:-.venv}"
  DELIMITER="----------------------------------------------------------------------"
  EXIT_CODE=0

  if ! [[ -e "Makefile" ]]; then
    cd -P "${script_base}" && pwd
  fi
  echo "PWD: ${PWD}"
  echo ""

  # Activate venv if it has been created.
  if [[ -d "${script_base}/${VENV_NAME}" ]] && [[ -e "${script_base}/${VENV_NAME}/bin/activate" ]]; then
    echo `date +"%Y-%m-%d %H:%M:%S"` "Activating existing ${VENV_NAME} ..."
    source "${script_base}/${VENV_NAME}/bin/activate"
    echo "${DELIMITER}"
    env|sort
    echo "${DELIMITER}"
    echo ""
  fi

  # Check venv again
  if [[ "${VIRTUAL_ENV}" != "" ]]; then
    echo `date +"%Y-%m-%d %H:%M:%S"` "Running '$@' in venv [${VIRTUAL_ENV}]"
    echo "${DELIMITER}"
    make $@
    EXIT_CODE=$?
  else
    rm -rf ${script_base}/${VENV_NAME}
    echo `date +"%Y-%m-%d %H:%M:%S"` "Creating python venv [${VENV_NAME}]"
    ${CMD_PY_VENV} ${script_base}/${VENV_NAME}
    source ${script_base}/${VENV_NAME}/bin/activate
    echo "${DELIMITER}"
    env|sort
    echo "${DELIMITER}"

    if [[ "${VIRTUAL_ENV}" == "${script_base}/${VENV_NAME}" ]]; then
      ${PIP_COMMAND} install --upgrade pip
      echo ""
      ${PIP_COMMAND} list
      echo "${DELIMITER}"
      make $@
      EXIT_CODE=$?
    else
      log_error "Cannot find or setup venv correctly."
    fi
  fi

  VENV_PATH="${VIRTUAL_ENV//${PWD}\//}"
  echo ""
  echo "Exit code = ${EXIT_CODE}"
  echo "${DELIMITER}"
  echo "Python environment: ${VIRTUAL_ENV}"
  echo "- Activate command: source ${VENV_PATH}/bin/activate"
  echo ""
  exit ${EXIT_CODE}
}

# check python version and environment
function check_python() {
  if [[ "${USE_PYTHON3}" =~ (1|enable|on|true|yes) ]]; then
    if [[ "${DEF_VERSION:0:1}" == "3" ]]; then
      CMD_PY_VENV="python -m venv"
      check_python_pip_
    elif [[ "${PY3_VERSION:0:1}" == "3" ]]; then
      PYTHON_EXEC="python3"
      CMD_PY_VENV="python3 -m venv"
      check_python_pip_ "3"
    else
      log_error "Cannot find python3."
    fi
  elif [[ "${USE_PYTHON2}" =~ (1|enable|on|true|yes) ]]; then
    if [[ "${PY2_VERSION:0:1}" == "2" ]]; then
      PYTHON_EXEC="python2"
      check_python_pip_ "2"
    elif [[ "${DEF_VERSION:0:1}" != "2" ]]; then
      log_error "Cannot find python2."
    fi
    if ! [[ -x "$(which virtualenv)" ]]; then
      log_error "Cannot find command 'virtualenv'."
    fi
    CMD_PY_VENV="virtualenv"
    check_python_pip_
  elif [[ "${DEF_VERSION:0:1}" == "3" ]]; then
    check_python_pip_
    CMD_PY_VENV="python -m venv"
    USE_PYTHON3="true"
  fi

  echo ""
  echo "Using $(${PYTHON_EXEC} --version 2>&1) [${CMD_PY_VENV}] ..."

  if [[ "${CMD_PY_VENV}" == "virtualenv" ]]; then
    if ! [[ -x "$(which virtualenv)" ]]; then
      log_error "Cannot find command 'virtualenv'."
    fi
  fi
}

# check python pip
function check_python_pip_() {
  set +u
  local _py_version_="${1}"  # should only be "", "2", or "3"
  local _python_pip_="pip${_py_version_//2/}"
  local _python_bin_="python${_py_version_//2/}"
  local _python_ver_="$( ${_python_bin_} -m pip -V 2>/dev/null | awk -F '[()]' '{print $2}')"

  if [[ "${_python_ver_}" != "" ]]; then
    PIP_COMMAND="${_python_bin_} -m pip"
  elif [[ -x "$(which ${_python_pip_})" ]]; then
    PIP_COMMAND="${_python_pip_}"
  else
    log_error "Cannot find command '${_python_pip_}'."
  fi
}

# log_error() func: exits with non-zero code on error unless $2 specified
function log_error() {
  set +u
  log_trace "$1" "ERROR" $2
}

# log_trace() func: print message at level of INFO, DEBUG, WARNING, or ERROR
function log_trace() {
  set +u
  local err_text="${1:-Here}"
  local err_name="${2:-INFO}"
  local err_code="${3:-1}"

  if [[ "${err_name}" == "ERROR" ]] || [[ "${err_name}" == "FATAL" ]]; then
    HAS_ERROR="true"
    echo ''
    echo '                                                      \\\^|^///  '
    echo '                                                     \\  - -  // '
    echo '                                                      (  @ @  )  '
    echo '----------------------------------------------------oOOo-(_)-oOOo-----'
    echo -e "\n${err_name}: ${err_text}" >&2
    echo '                                                            Oooo '
    echo '-----------------------------------------------------oooO---(   )-----'
    echo '                                                     (   )   ) / '
    echo '                                                      \ (   (_/  '
    echo '                                                       \_)       '
    echo ''
    exit ${err_code}
  else
    echo -e "\n${err_name}: ${err_text}"
  fi
}


check_python

# prevent from calling 'source $0' to close the console
[[ $0 != "${BASH_SOURCE}" ]] || main "$@"

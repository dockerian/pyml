#!/usr/bin/env bash
######################################################################
# Build AWS Lambda Function
#
# Command line arguments:
#   $1 - environment, e.g. 'dev', test' (default), 'prod'
#
######################################################################
set +x
script_file="$( readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo ${BASH_SOURCE[0]} )"
script_name="${script_file##*/}"
script_base="$( cd "$( echo "${script_file%/*}/.." )" && pwd )"
script_path="$( cd "$( echo "${script_file%/*}" )" && pwd )"
builds_path="${script_base}/builds"

PROJECT="ml"
FEATURE="${FEATURE:-pyml}"
BUILD_ENV="${1:-${BUILD_ENV:-test}}"
BUILD_PACKAGE="${FEATURE}-lambdas-${BUILD_ENV}.zip"
DEFAULT_BUILD="${PROJECT}-lambdas"
DEFAULT_ARTIFACT="${DEFAULT_BUILD}.zip"
SOURCE_DIR="${script_base}/${PROJECT}"
REQUIREMENTS="${SOURCE_DIR}/requirements.txt"
BUILDS_DIR="${BUILDS_DIR:-${builds_path}}"
README="${BUILDS_DIR}/BUILD-INFO.txt"

PYTHON_EXEC="python"
PY_LIB_PATH="$(pip show pip | grep Location | awk '{print substr($0, index($0,$2))}')"
DEF_VERSION="$(python  --version 2>&1 | grep 'Python' | awk '{print $2}')"
PY2_VERSION="$(python2 --version 2>&1 | grep 'Python' | awk '{print $2}')"
PY3_VERSION="$(python3 --version 2>&1 | grep 'Python' | awk '{print $2}')"
USE_PYTHON3="${USE_PYTHON3:-true}"
PIP_COMMAND="pip"


function main() {
  set +u
  shopt -s nocasematch
  for arg in $@ ; do
    if [[ "${arg}" =~ (help|/h|-\?|\/\?) ]] || [[ "${arg}" == "-h" ]]; then
      usage; return
    fi
  done
  if [[ "$@" =~ (--help|/help|-\?|/\?) ]]; then
    usage; return
  fi
  set -u

  check_python
  check_depends
  check_deploy_args

  echo ""
  echo "--- Building ${FEATURE} ---"
  echo ""
  build

  check_git_commit

  echo ""
  echo "${PROJECT} package is ready: ${builds_path}/${BUILD_PACKAGE}"
  echo "-----------------------------------------------------------------------"
  echo ""
}

function build() {
  local pip_args='--install-option="--prefix="'
  local conf_yml='<default config.yaml>'

  cd -P "${script_base}" && pwd
  rm -rf ${builds_path}/${FEATURE}
  rm -rf ${builds_path}/${BUILD_PACKAGE}
  mkdir -p ${builds_path}
  # cp -f "${script_base}/setup.cfg" "${script_base}/${PROJECT}/setup.cfg"
  echo "......................................................................."
  cat "${REQUIREMENTS}"
  echo "......................................................................."
  ${PIP_COMMAND} install --upgrade -r "${REQUIREMENTS}" \
    -t ${builds_path}/${FEATURE}
  echo "......................................................................."
  cp -rf ${SOURCE_DIR} ${builds_path}/${FEATURE}
  cp -rf ${SOURCE_DIR}/main.py ${builds_path}/${FEATURE}/handler.py
  rm -rf ${builds_path}/${FEATURE}/${PROJECT}/logging.yaml

  if [[ -e ${SOURCE_DIR}/config-${BUILD_ENV}.yaml ]]; then
    log_trace "- copying config-${BUILD_ENV}.yaml to build ..."
    cp -rf ${SOURCE_DIR}/config-${BUILD_ENV}.yaml ${builds_path}/${FEATURE}/config.yaml
    conf_yml=${SOURCE_DIR}/config-${BUILD_ENV}.yaml
    echo ""
  fi
  cd ${builds_path}/${FEATURE} && zip -r ../${BUILD_PACKAGE} .
  cd -P "${script_base}" && pwd

  echo ""
  echo "======================================================================="
  echo "NOTE: This build is using: ${conf_yml}"
  echo "======================================================================="
  log_trace "- removing ${builds_path}/${FEATURE} ..."
  rm -rf ${builds_path}/${FEATURE}
}

# check_depends(): verifies preset environment variables exist
function check_depends() {
  local conf_aws=""
  local tool_set="aws git jq tee tree"
  set +u
  echo "......................................................................."
  echo "Checking dependencies: ${tool_set}"
  for tool in ${tool_set}; do
    if ! [[ -x "$(which ${tool})" ]]; then
      log_error "Cannot find command '${tool}'"
    fi
  done
}

# check_git_commit(): check git commit and create build description
function check_git_commit() {
  echo ""
  echo "--- Checking build description ---"
  cd -P "${script_base}" && pwd
  local commit_sha="$(git rev-parse --short HEAD)"

  if [[ "${commit_sha}" != "" ]]; then
    git show ${commit_sha} --raw | tee "${README}"
    echo "----------------------------------------" >> "${README}"
    git branch -v | grep '^*' >> "${README}"
  fi
}

# check python version and environment
function check_python() {
  if [[ "${USE_PYTHON3}" =~ (1|enable|on|true|yes) ]]; then
    if [[ "${DEF_VERSION:0:1}" == "3" ]]; then
      check_python_pip_
    elif [[ "${PY3_VERSION:0:1}" == "3" ]]; then
      PYTHON_EXEC="python3"
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
    check_python_pip_
  elif [[ "${DEF_VERSION:0:1}" == "3" ]]; then
    check_python_pip_
  fi

  echo ""
  echo "Using $(${PYTHON_EXEC} --version 2>&1) [${PIP_COMMAND}] ..."

  if [[ "${PIP_COMMAND}" == "pip3" ]]; then
    if ! [[ -x "$(which pip3)" ]]; then
      log_error "Cannot find command 'pip3'."
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

# check_return_code(): checks exit code from last command
function check_return_code() {
  local return_code="${1:-0}"
  local action_name="${2:-AWS CLI}"

  if [[ "${return_code}" != "0" ]]; then
    log_fatal "${action_name} [code: ${return_code}]" ${return_code}
  else
    echo "Success: ${action_name}"
    echo ""
  fi
}

# log_error() func: exits with non-zero code on error unless $2 specified
function log_error() {
  set +u
  log_trace "$1" "ERROR" $2
}

# log_fatal() func: exits with non-zero code on fatal failure unless $2 specified
function log_fatal() {
  set +u
  log_trace "$1" "FATAL" $2
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

# usage() func: show help
function usage() {
  local headers="0"
  echo ""
  echo "USAGE: ${script_file} --help"
  echo ""
  # echo "$(cat ${script_path} | grep -e '^#   \$[1-9] - ')"
  while IFS='' read -r line || [[ -n "${line}" ]]; do
    if [[ "${headers}" == "0" ]] && [[ "${line}" =~ (^#[#=-\\*]{59}) ]]; then
      headers="1"
      echo "${line}"
    elif [[ "${headers}" == "1" ]] && [[ "${line}" =~ (^#[#=-\\*]{59}) ]]; then
      headers="0"
      echo "${line}"
    elif [[ "${headers}" == "1" ]]; then
      echo "${line}"
    fi
  done < "${script_path}"
}


[[ $0 != "${BASH_SOURCE}" ]] || main "$@"

#!/usr/bin/env bash
##############################################################################
# Checkout specific commit sha or revision tag from a branch
# Author: jason_zhuyx@hotmail.com
#
# Command line arguments:
#   $1 : git commit sha (or revision tag with --tag)
#   --tag : using revision tag instead of commit sha
#
# Expecting in git workspace having ".git" folder with optional
#   GIT_BRANCH (git branch, default to 'master')
#   GIT_REVISION_TAG (takes precedence, or using GIT_REVISION_SHA)
#   GIT_REVISION_SHA (or using current commit sha)
#       if no command line arguments is provided.
#
# ********
# CAUTION: This will RESET --HARD to ${GIT_BRANCH}. Use on a clean workspace.
# ********
#
# NOTE: Checking out revision tag or commit sha could detach from HEAD.
#       Recommend to reset back to origin/master by
#           git reset --hard
#           git checkout master && git reset --hard origin/master
#           git clean -d -x -f
#      Also disable pager on CI/CD server (e.g. Jenkins)
#           git config --global core.pager cat
#
##############################################################################
set -eo pipefail
# assuming this script is under ${script_base}/tools
script_file="$( readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo ${BASH_SOURCE[0]} )"
script_name="${script_file##*/}"
script_base="$( cd "$( echo "${script_file%/*}/.." )" && pwd )"
script_path="$( cd "$( echo "${script_file%/*}" )" && pwd )"

GIT_BRANCH="${GIT_BRANCH:-master}"
GIT_REVISION_SHA="${GIT_REVISION_SHA:-None}"
GIT_REVISION_TAG="${GIT_REVISION_TAG:-None}"
USE_REVISION_TAG="false"


# main entry
function main() {
  REVISION="${1:-None}"

  shopt -s nocasematch
  for arg in $@ ; do
    if [[ "${arg}" =~ (help|/h|-\?|\/\?) ]] || [[ "${arg}" == "-h" ]]; then
      usage; return
    fi
  done
  if [[ "$@" =~ (--help|/help|-\?|/\?) ]]; then
    usage; return
  fi

  echo ""
  cd -P "${script_base}" && pwd
  do_checkout "${REVISION}"

  git show
}

# check out git commit sha or revision tag
function do_checkout() {
  local github_rev="${1:-None}"
  local commit_sha="$(git rev-parse --short HEAD 2>/dev/null)"
  local commit_tag="$(git describe --tags --abbrev 2>/dev/null)"

  log_trace "--- Checking git commit sha or revision tag ---"

  if [[ "${commit_sha}" == "" ]]; then
    git show
    git rev-parse --short HEAD
    log_error "Failed to get git commit in ${PWD}"
  fi

  if [[ "${github_rev}" == "None" ]]; then
    if [[ "${GIT_REVISION_TAG}" != "None" ]]; then
      log_trace "Using git revision tag '${GIT_REVISION_TAG}'"
      github_rev="${GIT_REVISION_TAG}"
      USE_REVISION_TAG="true"
    elif [[ "${GIT_REVISION_SHA}" != "None" ]]; then
      log_trace "Using git commit SHA '${GIT_REVISION_SHA}'"
      github_rev="${GIT_REVISION_SHA}"
    fi
  elif [[ "${USE_REVISION_TAG}" == "true" ]]; then
    if [[ "${GIT_REVISION_TAG}" != "None" ]] && \
       [[ "${GIT_REVISION_TAG}" != "${github_rev}" ]]; then
         rev_info="revision [${github_rev}]"
         tag_info="GIT_REVISION_TAG [${GIT_REVISION_TAG}]"
         log_trace "${tag_info} does not match to input ${rev_info}" WARNING
    fi
  elif [[ "${GIT_REVISION_SHA}" != "None" ]] && \
       [[ "${GIT_REVISION_SHA}" != "${github_rev}" ]]; then
         rev_info="revision [${github_rev}]"
         sha_info="GIT_REVISION_SHA [${GIT_REVISION_SHA}]"
         log_trace "${sha_info} does not match to input ${rev_info}" WARNING
  fi
  if [[ "${github_rev}" != "None" ]]; then
    log_trace "--- Resetting branch  ---"
    git reset --hard
    log_trace "--- Checking out branch ${GIT_BRANCH} ---"
    git checkout ${GIT_BRANCH} && git reset --hard origin/${GIT_BRANCH}
    log_trace "--- Cleaning up git workspace ${PWD} ---"
    git clean -d -x -f

    if [[ "${USE_REVISION_TAG}" == "true" ]]; then
      log_trace "--- Checking out revision tag [${github_rev}] ---"
      # git checkout -f -q --no-progress tags/${github_rev}  # NOTE: this is detaching from HEAD
      git reset -q --hard "${github_rev}"
    elif [[ "${github_rev}" != "${commit_sha}" ]]; then
      log_trace "--- Checking out revision sha [${github_rev}] ---"
      # git checkout -f -q --no-progress ${github_rev}  # NOTE: this is detaching from HEAD
      git reset -q --hard "${github_rev}"
    fi
  else
    log_trace "--- Using current commit [${commit_sha}] ---"
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
    echo -e "\n${err_name}: ${err_text}" >&2
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


ARGS=""
# pre-processing optional arguments
for arg in $@; do
  if [[ "${arg}" =~ "--" ]]; then
    if [[ "${arg}" =~ "--tag" ]]; then
      USE_REVISION_TAG="true"
    fi
  else
    ARGS="${ARGS} "${arg}""
  fi
done


[[ $0 != "${BASH_SOURCE}" ]] || main "$@"

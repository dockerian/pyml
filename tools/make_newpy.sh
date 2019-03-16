#!/usr/bin/env bash
############################################################
# Bash CLI to create a new python3 project                 #
#                                                          #
# Author: Jason Zhu (https://github.com/dockerian)         #
#                                                          #
# Arg options:                                             #
#   --install [<bin/path>] | --uninstall | --dry-run       #
#                                                          #
# Prerequsite:                                             #
#   - docs/templ/* and tools/*.sh                          #
#   - Linux shell commands: find git readlink sed tr       #
#   - github user or organization name (recommended)       #
#   - registered docker hub user or organization name      #
#   - git-configured 'user.name' and 'user.email'          #
#   - current directory in a cloned repository (optional)  #
#   - docker installed and logged in (optional)            #
#                                                          #
############################################################
set +x
script_bash="${BASH_SOURCE[0]}"
script_file="$( readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo ${BASH_SOURCE[0]} )"
script_name="${script_file##*/}"
script_base="$( cd "$( echo "${script_file%/*}/.." )" && pwd )"
script_path="$( cd "$( echo "${script_file%/*}" )" && pwd )"
docker_user="$( docker info 2>/dev/null|sed '/Username:/!d;s/.* //' )"
script_file="${script_path}/${script_name}"

__DRY_RUN__="${DRY_RUN:-false}"
_COPY_BASE_="example"
_TEMP_PATH_="/tmp/__new_python_project_templ__"
_TMPL_PATH_="${script_base}/docs/templ"
_TOOL_PATH_="${script_base}/tools"
_DELIMITER_="------------------------------------------------------------------------"
_DOT_SPLIT_="........................................................................"
_BOX_TITLE_="
╔════════════════════════════════╗
║ make_newpy.sh © 2019 Jason Zhu ║
╚════════════════════════════════╝
"

# all user inputs
__AUTHOR_NAME__="$(git config --get user.name 2>/dev/null)"
__AUTHOR_EMAIL__="$(git config --get user.email 2>/dev/null)"
__CODECOV_TOKEN__="${CODECOV_TOKEN}"
__DOCKER_CONTAINER_NAME__=
__DOCKER_USER_OR_ORGANIZATION_NAME__="${DOCKER_USER:-${docker_user:-dockerian}}"
__GITHUB_USER_OR_ORGANIZATION__=
__GITHUB_REPOSITORY_NAME__=""
__GITHUB_USER__="${GITHUB_USERNAME:-dockerian}"  # temporary variable
__GITHUB_REPO__=""  # temporary variable
__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__=
__PROJECT_LOG_NAME__=
__PROJECT_CODE_NAME__=
__PROJECT_DESCRIPTION__=
__PROJECT_SUBJECT__="Software"
__PROJECT_TITLE__=
__PROJECT_URL__=
__REPOSITORY_DIRECTORY__=""
__TEST_COVERAGE_THRESHOLD__="90"
__VERSION__="1.0.0"



# main function
function main() {

  check_depends

  check_all_inputs
  display_inputs "yes" || return

  copy_templates
  create_new
}

function check_args() {
  shopt -s nocasematch
  for arg in $@ ; do
    if [[ "${arg}" =~ (help|/h|-\?|\/\?) ]] || [[ "${arg}" == "-h" ]]; then
      usage; return
    fi
  done
  if [[ "$@" =~ (--help|/help|-\?|/\?) ]]; then
    usage; return
  fi
  echo "${_SIG_TITLE_}"
  if [[ "$1" =~ install$ ]] || [[ "$1" =~ setup ]]; then
    do_install "$1" "$2"; return
  fi
  if [[ "$@" =~ (--dry-run|/dry|-dry|dry-?run) ]]; then
    log_trace "Dry-run MODE: on" WARNING
    __DRY_RUN__="true"
  fi

  main "$@"
}

function check_all_inputs() {

  check_input_path
  check_input_python_module
  check_input_project_info
  check_input_docker_hostname
  check_input_docker_user
  check_input_author
  check_input_author_email

  echo ""
# check_input_codecov_token
  check_input_percentage
}

function check_confirmation() {
  local _query_="${1:-Continue to process}"
  local _stdin_=""

  read -p "${_query_} (y/n): " _stdin_
  echo ""

  shopt -s nocasematch
  if [[ ! "${_stdin_}" =~ ^(continue|okay|sure|yes|y)$ ]]; then
    return 9  # false on confirmation
  fi
  return 0
}

function check_depends() {
  local _tool_set_="find git sed tr"
  set +u
  for cmd in ${_tool_set_}; do
    if ! [[ -x "$(which ${cmd})" ]]; then
      log_error "Cannot find command: '${cmd}'"
    fi
  done
}

function check_input_author() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^([A-Z][a-zA-Z-]{0,19}.?)( [a-zA-Z-]{1,19}\.?){1,2}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Author's name (${__AUTHOR_NAME__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__AUTHOR_NAME__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __AUTHOR_NAME__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Author name should contain more than one ASCII char, per regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
      echo '    and in format of "<First-Name> <Last-Name>".'
      echo ''
    fi
  done
}

# see http://emailregex.com/
function check_input_author_email() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Author e-mail (${__AUTHOR_EMAIL__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__AUTHOR_EMAIL__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __AUTHOR_EMAIL__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Author email should contain more than one ASCII char, per regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
      echo '    and in format of "<user.alias>@<domain.name>".'
      echo ''
    fi
  done
}

function check_input_codecov_token() {
  local _stdin_=''
  local _retry_='2'
  local _regex_='^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
  while [[ "${_retry_}" -gt 0 ]]; do
    read -p "Codecov token (${__CODECOV_TOKEN__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__CODECOV_TOKEN__}" =~ ${_regex_} ]]; then
      _retry_="0"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __CODECOV_TOKEN__="${_stdin_}"
      _retry_="0"
    else
      echo "${_DOT_SPLIT_}"
      echo "Codecov token should only contain letters, digits, and '-' (dash):"
      echo ""
      echo "    ${_regex_}"
      echo ''
      echo 'Each repository requires a unique token to upload codecov report'
      echo 'See https://docs.codecov.io/docs'
      echo ''
      _retry_="$((${_retry_} - 1))"
    fi
  done
}

function check_input_docker_hostname() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[a-z][-a-z]{1,15}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Docker host/image's name (${__DOCKER_CONTAINER_NAME__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__DOCKER_CONTAINER_NAME__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __DOCKER_CONTAINER_NAME__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo "Docker host/image's name is validated by regex:"
      echo ''
      echo "    ${_regex_}"
      echo ''
    fi
  done
}

function check_input_docker_user() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[a-z][a-z0-9]{1,19}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Docker user/organization (${__DOCKER_USER_OR_ORGANIZATION_NAME__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__DOCKER_USER_OR_ORGANIZATION_NAME__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __DOCKER_USER_OR_ORGANIZATION_NAME__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Docker user or organization name is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
      echo '    see https://hub.docker.com/signup'
      echo ''
    fi
  done
}

function check_input_github_repo() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[a-zA-Z][-0-9a-zA-Z_]{1,19}[0-9a-zA-Z]$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Github repository's name (${__GITHUB_REPO__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__GITHUB_REPO__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __GITHUB_REPO__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Github repository name is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
      echo '    see https://help.github.com/en'
      echo ''
    fi
  done
}

function check_input_github_user() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[a-zA-Z][-0-9a-zA-Z_]{1,19}[0-9a-zA-Z]$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Github user/organization (${__GITHUB_USER__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__GITHUB_USER__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __GITHUB_USER__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Github user or organization name is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
      echo '    see https://help.github.com/en'
      echo ''
    fi
  done
}

function check_input_path() {
  local _stdin_=''
  local _valid_='false'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "New project root/top dir (${__REPOSITORY_DIRECTORY__:-N/A}): " _stdin_

    if [[ "${_stdin_}" =~ ^\s*$ ]]; then
      _stdin_="${PWD}"
    fi
    _stdin_="${_stdin_/\~/${HOME}}"

    check_repo_dir "${_stdin_}" || continue
    check_repo_local_path "${_stdin_}"

    if [[ "${__GITHUB_REPO__}" == "" ]] || [[ "${__GITHUB_USER__}" == "" ]]; then
      check_input_github_user
      check_input_github_repo
    fi

    local _dpath_="$( cd "${_stdin_}" 2>/dev/null && pwd || echo "${_stdin_}" )"
    if [[ ! -d "${_stdin_}" ]]; then
      mkdir -p "${_stdin_}" 2>/dev/null
      _dpath_="$( cd "${_stdin_}" 2>/dev/null && pwd )"
      rm -rf "${_stdin_}" 2>/dev/null
    fi
    __REPOSITORY_DIRECTORY__="${_dpath_:-${_stdin_}}"
    __GITHUB_USER_OR_ORGANIZATION__="${__GITHUB_USER__}"
    __GITHUB_REPOSITORY_NAME__="${__GITHUB_REPO__}"
    _valid_="true"
  done

  local _s_url_="https://github.com/${__GITHUB_USER__}/${__GITHUB_REPO__}"
  __PROJECT_URL__="${__PROJECT_URL__:-${_s_url_}}"

  local _regex_='([a-zA-Z][0-9a-zA-Z]{1,15})$'
  if [[ "${__GITHUB_REPOSITORY_NAME__}" =~ ${_regex_} ]]; then
    __PYTHON_MODULE__="${BASH_REMATCH[1]}"
  elif [[ "${__REPOSITORY_DIRECTORY__}" =~ ${_regex_} ]]; then
    __PYTHON_MODULE__="${BASH_REMATCH[1]}"
  fi
}

function check_input_percentage() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^(100|[1-9][0-9])$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Code coverage threshold (${__TEST_COVERAGE_THRESHOLD__} %): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__TEST_COVERAGE_THRESHOLD__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __TEST_COVERAGE_THRESHOLD__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Code coverage threshold is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
    fi
  done
}

function check_input_project_codename() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[A-Z][-a-zA-Z0-9]{1,15}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Project codename (${__PROJECT_CODE_NAME__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__PROJECT_CODE_NAME__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __PROJECT_CODE_NAME__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Project codename is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
    fi
  done
}

function check_input_project_info() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[A-Z][-~a-zA-Z_.0-9 ]{5,25}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Project title (${__PROJECT_TITLE__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__PROJECT_TITLE__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __PROJECT_TITLE__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Project title is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
    fi
  done

  check_input_project_codename
  check_input_version
  check_input_subject

  read -p "Project description (optional): " __PROJECT_DESCRIPTION__
  read -p "Project URL (${__PROJECT_URL__:-N/A}): " __url__

  __url__="${__url__//\'/_}"
  __PROJECT_DESCRIPTION__="${__PROJECT_DESCRIPTION__//\'/_}"
  __PROJECT_URL__="${__url__:-${__PROJECT_URL__}}"
}

function check_input_python_module() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[a-zA-Z][0-9a-zA-Z_]{1,15}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Project top level module (${__PYTHON_MODULE__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__PYTHON_MODULE__}" =~ ${_regex_} ]]; then
      __PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__="${__PYTHON_MODULE__}"
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __PYTHON_MODULE__="${_stdin_}"
      __PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Project top level python module name is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
      echo '    recommend to use a short name in snake_case style.'
      echo ''
    fi
  done

  __DOCKER_CONTAINER_NAME__="${__PYTHON_MODULE__}"
  __PROJECT_LOG_NAME__="__${__PYTHON_MODULE__}__.log"

  local _modux_="${__PYTHON_MODULE__:-Python3}"
  local _codex_=`echo ${_modux_:0:1}|tr '[a-z]' '[A-Z]'`"${_modux_:1}"
  __PROJECT_TITLE__="${__PROJECT_TITLE__:-${_codex_}} Project"
  __PROJECT_CODE_NAME__="${__PROJECT_CODE_NAME__:-${_codex_}}"
}

function check_input_subject() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[A-Z][-a-zA-Z]{1,19}( [A-Z][-a-zA-Z]{1,19})?$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Project subject (${__PROJECT_SUBJECT__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__PROJECT_SUBJECT__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __PROJECT_SUBJECT__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Project subject is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
    fi
  done
}

function check_input_version() {
  local _stdin_=''
  local _valid_='false'
  local _regex_='^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,8}$'
  while [[ "${_valid_}" == "false" ]]; do
    read -p "Project version (${__VERSION__:-N/A}): " _stdin_
    if [[ "${_stdin_}" =~ ^\s*$ ]] && [[ "${__VERSION__}" =~ ${_regex_} ]]; then
      _valid_="true"
    elif [[ "${_stdin_}" =~ ${_regex_} ]]; then
      __VERSION__="${_stdin_}"
      _valid_="true"
    else
      echo "${_DOT_SPLIT_}"
      echo 'Project version is validated by regex:'
      echo ''
      echo "    ${_regex_}"
      echo ''
    fi
  done
}

function check_repo_dir() {
  local _dir_="$( cd "$1" 2>/dev/null && pwd || echo "$1" )"
  local _new_="true"

  for file in .dockerignore .gitignore .pylintc .travis.ym \
      Dockerfile Makefile README.md setup.py setup.cfg tests tools; do
    if [[ -e "${_dir_}/${file}" ]]; then _new_="false"; fi
  done

  local _stdin_=""
  if [[ "${_new_}" == "true" ]]; then
    if [[ ! -e "${_dir_}" ]]; then return 0; fi
    echo ""
    echo "Existing directory: ${_dir_}"
    echo "${_DOT_SPLIT_}"
    ls -al "${_dir_}"
    echo "${_DELIMITER_}"

    check_confirmation "Confirm to use this directory" || return 1

    return 0
  fi

  echo ""
  echo "Existing contents in repository directory (${_dir_}):"
  echo "${_DOT_SPLIT_}"
  ls -al "${_dir_}"
  echo ""
  echo "${_DOT_SPLIT_}"
  echo 'New project root should be:'
  echo '  * a writable local directory'
  echo '  * cloned from a valid git, e.g. github, repository'
  echo '  * okay to overwrite existing files and directories:'
  echo '    - Folder: tools (all bash scripts)'
  echo '    - Folder: tests (all python test data and code)'
  echo '    - .dockerignore, .gitignore, .pylintc, .travis.yml'
  echo '    - Dockerfile, Makefile, and READEM.md'
  echo '    - setup.py and setup.cfg'
  echo ''
  echo "${_DELIMITER_}"

  check_confirmation "Confirm to allow overwritting" || return 3

  return 0
}

function check_repo_dir_creatable() {
  local _dir_="$1"
  local _new_="false"

  if [[ ! -d "${_dir_}" ]]; then
    if [[ -e "${_dir_}" ]]; then
      log_error "Cannot create directory '${_dir_}' - already exists."
    fi
    _new_="true"
  fi

  mkdir -p "${_dir_}" || log_error "Cannot create directory '${_dir_}'."

  check_repo_dir_writtable "${_dir_}"

  if [[ "${_new_}" == "true" ]]; then
    rm -rf "${_dir_}" || log_error "Cannot delete directory '${_dir_}'."
  fi
}

function check_repo_dir_writtable() {
  local _dir_="$1"
  local _pwd_="${PWD}"
  local _err_=""

  if [[ ! -d "${_dir_}" ]]; then
    log_error "Cannot find directory '${_dir_}'"
  fi

  cd -P "${_dir_}" || log_error "Cannot change to '${_dir_}'"

  local _tmp_dir_="__tmp__.tmp"
  local _tmp_sub_="${_tmp_dir_}/__foo__/__bar__/__abc__"
  local _tmp_new_="__new__.tmp"
  set +x
  rm -rf "${_tmp_dir_}" 1>/dev/null 2>&1
  mkdir -p "${_tmp_sub_}" 1>/dev/null 2>&1
  if [[ ! -d "${_tmp_sub_}" ]]; then
    _err_="Cannot create directory in '${_dir_}'"
  fi
  echo "adding new line" 1>"${_tmp_sub_}/${_tmp_new_}" 2>/dev/null
  if [[ ! -e "${_tmp_sub_}/${_tmp_new_}" ]]; then
    _err_="Cannot create file in '${_dir_}'"
  fi
  rm -rf "${_tmp_dir_}" 1>/dev/null 2>&1
  if [[ -d "${_tmp_dir_}" ]]; then
    _err_="Cannot write to '${_dir_}'"
  fi
  rm -rf "${_TEMP_PATH_}" 1>/dev/null 2>&1
  mkdir -p "${_TEMP_PATH_}" 1>/dev/null 2>&1
  if [[ ! -d "${_TEMP_PATH_}" ]]; then
    _err_="Cannot create '${_TEMP_PATH_}'"
  fi

  # return back to original $PWD
  cd "$_pwd_"

  if [[ "${_err_}" != "" ]]; then
    log_error "${_err_}."
  fi
}

function check_repo_local_path() {

  local _dir_="$1"
  local _pwd_="${PWD}"
  local _new_=""

  check_repo_dir_creatable "${_dir_}"

  if [[ ! -d "${_dir_}" ]]; then
    mkdir -p "${_dir_}" 2>/dev/null || log_error "Cannot create path: ${_dir_}"
    _new_="true"
  fi

  cd -P "${_dir_}" || log_error "Cannot change path: ${_dir_}"

  local _url_="$(git ls-remote --get-url upstream 2>/dev/null)"
  if [[ "${_url_}" == "" ]] || [[ "${_url_}" == "upstream" ]]; then
    # getting default remote URL if upstream is not set
    _url_="$(git ls-remote --get-url 2>/dev/null)"
  fi

  check_repository "${_url_}"

  if [[ "${_new_}" == "true" ]]; then
    rm -rf "${_dir_}" 2>/dev/null || log_error "Cannot remove path: ${_dir_}"
  fi
  # return back to original $PWD
  cd "$_pwd_"
}

function check_repository() {
  local _repo_="$1"
  # full regex: ^((file|git|rsync|ssh|https?):\/\/|(git|user)@)([-a-z\/~@\:_.]+?)[:\/]([a-zA-Z\-_.]+)\/([a-zA-Z\-_.]+)\.git\/?$
  local _regx_='((git|https?):\/\/|(git)@)([-a-z\/_.]+?)[:\/]([-a-zA-Z_.]+)\/([-a-zA-Z_.]+)\.git'
  if [[ "${_repo_}" =~ ([-a-zA-Z_.]+)\/([-a-zA-Z_.]+)\.git ]]; then
    __GITHUB_USER__="${BASH_REMATCH[1]}"
    __GITHUB_REPO__="${BASH_REMATCH[2]}"
    echo "${_DOT_SPLIT_}"
    echo "Github repository: ${_repo_}"
    echo "       - org/user: ${__GITHUB_USER__}"
    echo "       - repo dir: ${__GITHUB_REPO__}"
    echo ""
  else
    __GITHUB_REPO__=""
  fi
}

# copy template files for project structure
function copy_templates() {
  local _src_path_="${_TMPL_PATH_}"
  local _dst_path_="${_TEMP_PATH_}"
  log_trace "Creating templates into ${_dst_path_}"

  rm -rf "${_dst_path_}"
  mkdir -p "${_dst_path_}"
  cp -Rf "${_src_path_}/${_COPY_BASE_}" "${_dst_path_}"

  local _pym_="${__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__:-${__PYTHON_MODULE__}}"
  local _dir_="${_dst_path_}/${_COPY_BASE_}/${_pym_}"
  local _msg_="Cannot create python module: ${_dir_}"
  mv "${_dst_path_}/${_COPY_BASE_}/proj" "${_dir_}" || log_error "${_msg_}"

  local _IFS_SAVE_=$IFS
  IFS=$(echo -en "\n\b")
  log_trace "Updating templ files in ${_dst_path_}/${_COPY_BASE_}"
  for _file_ in $( find "${_dst_path_}/${_COPY_BASE_}" -name \*.templ -type f ); do
    if [[ "${__DRY_RUN__}" == "true" ]]; then
      echo "  ::: dry-run processing file ${_file_}"
    else
      create_project_file "${_file_}"
    fi
  done
  IFS="${_IFS_SAVE_}"

  if [[ "${__DRY_RUN__}" != "true" ]]; then
    log_trace "Cleaning templ files in ${_dst_path_}"
    find "${_dst_path_}" -name \*.templ -type f -delete
  fi

  log_trace "Copying all templ files ${_src_path_}"
  mkdir -p "${_dst_path_}/docs" || log_error "Cannot copy templ files"
  cp -Rf "${_src_path_}" "${_dst_path_}/docs"
}

function create_new() {
  local _src_path_="${_TEMP_PATH_}"
  local _dst_path_="${__REPOSITORY_DIRECTORY__}"
  local _dot_pads_="$( echo ${_dst_path_}|sed 's/./─/g')"
  local _sps_pads_="$( echo ${_dst_path_}|sed 's/./ /g')"

  if [[ "${__DRY_RUN__}" == "true" ]]; then
    log_trace "Complete dry-run new in ${_src_path_}"
    return 0
  fi

  log_trace "Creating new project in ${_dst_path_}"
  local _msg_="Failed creating project ${_dst_path_}"
  mkdir -p "${_dst_path_}/docs" || log_error "${_msg_}"
  mkdir -p "${_dst_path_}/tools" || log_error "${_msg_}"
  cp -aRf "${_TOOL_PATH_}" "${_dst_path_}" || log_error "${_msg_}"
  cp -aRf "${_src_path_}/docs" "${_dst_path_}" || log_error "${_msg_}"
  cp -Rf "${_src_path_}/${_COPY_BASE_}"/* "${_dst_path_}" || log_error "${_msg_}"
  cp -f "${_src_path_}/${_COPY_BASE_}"/.* "${_dst_path_}" 2>/dev/null

  echo ""
  echo "${_DELIMITER_}"
  local _pad_begin_="Complete new project in ─────┐"
  local _pad_="                                   │"
  log_trace "${_pad_begin_}\n${_pad_}"
  echo -e "\t─── ${_dst_path_}"
  echo "${_BOX_TITLE_}"
  echo ":: DONE ::"
  echo ""
}

function create_project_file() {
  local _src_="${1:-none}"
  local _dst_="${_src_//.templ/}"

  if [[ "${_src_}" == "${_dst_}" ]]; then return; fi
  if [[ ! -f "${_src_}" ]]; then
    log_trace "Cannot open source file: ${_src_}" WARNING
    return
  fi

  local _pym_="${__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__:-${__PYTHON_MODULE__}}"
  while IFS='' read -r _line || [[ -n "${_line}" ]]; do
    _line="${_line//\{\{__AUTHOR_NAME__\}\}/${__AUTHOR_NAME__}}"
    _line="${_line//\{\{__AUTHOR_EMAIL__\}\}/${__AUTHOR_EMAIL__}}"
    _line="${_line//\{\{__CODECOV_TOKEN__\}\}/${__CODECOV_TOKEN__}}"
    _line="${_line//\{\{__DOCKER_CONTAINER_NAME__\}\}/${__DOCKER_CONTAINER_NAME__}}"
    _line="${_line//\{\{__DOCKER_USER_OR_ORGANIZATION_NAME__\}\}/${__DOCKER_USER_OR_ORGANIZATION_NAME__}}"
    _line="${_line//\{\{__GITHUB_USER_OR_ORGANIZATION__\}\}/${__GITHUB_USER_OR_ORGANIZATION__}}"
    _line="${_line//\{\{__GITHUB_REPOSITORY_NAME__\}\}/${__GITHUB_REPOSITORY_NAME__}}"
    _line="${_line//\{\{__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__\}\}/${_pym_}}"
    _line="${_line//\{\{__PROJECT_LOG_NAME__\}\}/${__PROJECT_LOG_NAME__}}"
    _line="${_line//\{\{__PROJECT_CODE_NAME__\}\}/${__PROJECT_CODE_NAME__}}"
    _line="${_line//\{\{__PROJECT_DESCRIPTION__\}\}/${__PROJECT_DESCRIPTION__}}"
    _line="${_line//\{\{__PROJECT_SUBJECT__\}\}/${__PROJECT_SUBJECT__}}"
    _line="${_line//\{\{__PROJECT_TITLE__\}\}/${__PROJECT_TITLE__}}"
    _line="${_line//\{\{__PROJECT_URL__\}\}/${__PROJECT_URL__}}"
    _line="${_line//\{\{__REPOSITORY_DIRECTORY__\}\}/${__REPOSITORY_DIRECTORY__}}"
    _line="${_line//\{\{__TEST_COVERAGE_THRESHOLD__\}\}/${__TEST_COVERAGE_THRESHOLD__}}"
    _line="${_line//\{\{__VERSION__\}\}/${__VERSION__}}"
    echo  "${_line}"
  done  < "${_src_}" >> "${_dst_}"
}

function display_inputs() {
  local _confirm_="${1:-none}"
  local _newpath_="${__REPOSITORY_DIRECTORY__}"
  local _dir_tag_="$( [[ -d "${_newpath_}" ]] && echo "[exists]" )"

  echo ""
  echo "${_DOT_SPLIT_}"
  echo "              Python module : ${__PROJECT_FOLDER_AS_PYTHON_TOP_MODULE_NAME__}."
  echo "              Project title : ${__PROJECT_TITLE__}"
  echo "   Project codename/version : ${__PROJECT_CODE_NAME__} ${__VERSION__}"
  echo "        Project description : ${__PROJECT_DESCRIPTION__}"
  echo "            Project subject : ${__PROJECT_SUBJECT__}"
  echo "                Project URL : ${__PROJECT_URL__}"
  echo "        Author/creator info : ${__AUTHOR_NAME__} <${__AUTHOR_EMAIL__}>"
  echo "Github user or organization : ${__GITHUB_USER_OR_ORGANIZATION__}"
  echo "     Github repository name : ${__GITHUB_REPOSITORY_NAME__}"
  echo "Docker user or organization : ${__DOCKER_USER_OR_ORGANIZATION_NAME__}"
  echo "      Docker container name : ${__DOCKER_CONTAINER_NAME__}"
  echo "   Test covergage threshold : ${__TEST_COVERAGE_THRESHOLD__} %"
  echo "Project/repository top path : ${__REPOSITORY_DIRECTORY__} ${_dir_tag_:-[new]}"
  echo "       Project logfile name : ${__PROJECT_LOG_NAME__}"
  echo "              Codecov token : ${__CODECOV_TOKEN__}"
  echo "${_DOT_SPLIT_}"
  echo ""

  if [[ ! "${_confirm_}" =~ (true|yes) ]]; then return 0; fi

  local _retries_="5"
  while [[ "${_retries_}" -gt 0 ]]; do
    check_confirmation "Continue to create above project" && return 0
    _retries_="$(( ${_retries_} - 1 ))"
  done

  return 9
}

function display_result() {
  return
}

function do_install() {
  local cmd_link="${2:-/usr/local/bin/newpy}"
  local cmd_path="$( getpath "${cmd_link}" )"

  if [[ -e "${cmd_link}" ]]; then
    if [[ "${cmd_link}" == "${cmd_path}" ]]; then
      log_trace "Path '${cmd_link}' already exists." CAUTION
    elif [[ ! "$1" =~ uninstall$ ]]; then
      log_trace "Link '${cmd_link}' => '${cmd_path}' already exists." CAUTION
    else
      log_trace "Uninstalling/removing '${cmd_link}' ..."
      unlink "${cmd_link}" 2>/dev/null
      log_trace "Uninstalled/unlinked: '${cmd_link}'."
      return
    fi
    echo "...................................................................."
    ls -al "${cmd_link}"
    echo "...................................................................."
  elif [[ "$1" =~ uninstall$ ]]; then
    local _bash_path_="$( getpath "${script_bash}" )"
    local _full_path_="$( getfullpath "${script_bash}" )"
    if [[ "${_bash_path_}" != "${_full_path_}" ]]; then
      unlink "${_full_path_}" 2>/dev/null && \
      log_trace "Uninstalled/unlinked: '${_full_path_}'."
    else
      log_trace "Not found '${cmd_link}'."
    fi
  else
    log_trace "Installing '${script_file}' to '${cmd_link}' ..."
    unlink "${cmd_link}" 2>/dev/null || true
    log_trace "Settting '${cmd_link}' => '${script_file}'"
    ln -s "${script_file}" "${cmd_link}"
  fi
}

# getlink() func: gets the real path of a link, following all links
function getlink() {
  if [[ ! -h "$1" ]]; then
    echo "$1"
  else
    local link="$(expr "$(command ls -ld -- "$1")" : '.*-> \(.*\)$')"
    cd $(dirname $1)
    getlink "$link" | sed "s|^\([^/].*\)\$|$(dirname $1)/\1|"
  fi
}

# getfullpath() func:
# returns the absolute path to a command, $PATH (which) or not;
# returns the same if not found.
function getfullpath() {
  echo $1 | sed "s|^\([^/].*/.*\)|$(pwd)/\1|;s|^\([^/]*\)$|$(which -- $1 2>/dev/null)|;s|^$|$1|";
}

# getpath() func: returns the realpath of a called command.
# - dependencies: func getfullpath and getlink
function getpath() {
  local SCRIPT_PATH=$(getfullpath $1)
  getlink ${SCRIPT_PATH} | sed "s|^\([^/].*\)\$|$(dirname ${SCRIPT_PATH})/\1|";
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

# usage() func: show help
function usage() {
  local headers="o"
  echo ""
  echo "USAGE: ${script_name} --help"
  echo ""
  # echo "$(cat ${script_file} | grep -e '^#   \$[1-9] - ')"
  while IFS='' read -r line || [[ -n "${line}" ]]; do
    if [[ "${headers}" == "o" ]] && [[ "${line}" =~ (^#[#=-\\*]{59}) ]]; then
      headers="x"
      echo "${line}"
    elif [[ "${headers}" == "x" ]] && [[ "${line}" =~ (^#[#=-\\*]{59}) ]]; then
      headers="o"
      echo "${line}"
    elif [[ "${headers}" == "x" ]]; then
      echo "${line}"
    fi
  done < "${script_file}"
}

_SIG_TITLE_="
+================================+
| make_newpy.sh © 2019 Jason Zhu |
+================================+
"


# prevent from calling 'source $0' to close the console
[[ $0 != "${BASH_SOURCE}" ]] || check_args "$@"

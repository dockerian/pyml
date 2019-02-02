#!/usr/bin/env bash
##############################################################################
# Encrypt plaintext by AWS KMS Key
#
# Command line arguments:
#   $1 - plaintext (string), or fileb://File (e.g. fileb:///home/user/a.txt)
# or
#   --list    : to list all KMS keys (with available Arn and Alias info)
#             : or list key info per specified key id/arn/alias in $2
#   --decrypt : to decrypt from cipher text (in $2)
#
# Output
#   <stdout>  : encrypted text (CiphertextBlob)
#             : with full logging if DEBUG=1 [in environment]
#
# Dependencies:
#   - aws (aws cli), base64, jq (command-line JSON processor)
#   - an aws kms key (default 'aws-kms-key') with associated AWS role
#   - network connected to https://kms.us-east-1.amazonaws.com
#
# Expecting the runtime host is assigned with proper AWS Role;
# or from ~/.aws or the following environment variables (see check_depends)
#   AWS_ACCESS_KEY_ID
#   AWS_SECRET_ACCESS_KEY
#   AWS_DEFAULT_REGION (optional)
#   KMS_KEY_ID (optional)
#
##############################################################################
# set -eo pipefail
script_file="$( readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo ${BASH_SOURCE[0]} )"
script_name="${script_file##*/}"
script_base="$( cd "$( echo "${script_file%/*}/.." )" && pwd )"
script_path="$( cd "$( echo "${script_file%/*}" )" && pwd )"
kmskey_name="${KMS_KEY_ID:-aws-kms-key}"  # can be id, arn, alias
kmskey_list=""
kalias_list=""

# main entrance
function main() {
  shopt -s nocasematch
  for arg in $@ ; do
    if [[ "${arg}" =~ (help|/h|-\?|\/\?) ]] || [[ "${arg}" == "-h" ]]; then
      usage; return
    fi
  done
  if [[ "$@" =~ (--help|/help|-\?|/\?) ]]; then
    usage; return
  fi

  if [[ ! "${DEBUG:-0}" =~ (0|off|false|no) ]]; then
    DEBUG=1
  else
    DEBUG=0
  fi

  check_depends

  if [[ "$1" == "--decrypt" ]]; then
    decrypt_ciphertext "$2"
    return
  fi

  if [[ "$1" == "--list" ]]; then
    list_keys "$2"
    return
  fi

  if [[ "$1" != "" ]]; then
    encrypt "$1"
  fi
}

# check_depends(): verifies preset environment variables exist
function check_depends() {
  local tool_set="aws base64 jq"
  set +u
  if [[ "${DEBUG}" == "1" ]]; then
    echo "......................................................................."
    echo "Checking dependencies: ${tool_set}"
  fi
  for tool in ${tool_set}; do
    if ! [[ -x "$(which ${tool})" ]]; then
      log_error "Cannot find command '${tool}'"
    fi
  done

  if [[ "${kalias_list}" == "" ]]; then
    if [[ "${DEBUG}" == "1" ]]; then
      echo "Checking list of aws kms key aliases ..."
    fi
    kalias_list="$(aws kms list-aliases --output json 2>/dev/null)"
  fi

  if [[ "${kalias_list}" == "" ]]; then
    aws kms list-aliases 1>/dev/null
    log_error 'Failed to get key aliases by `aws kms list-aliases`.'
  fi

  if [[ "${kmskey_list}" == "" ]]; then
    if [[ "${DEBUG}" == "1" ]]; then
      echo "Checking list of aws kms keys ..."
    fi
    kmskey_list=$(aws kms list-keys --output json 2>/dev/null)
  fi

  if [[ "${kmskey_list}" == "" ]]; then
    aws kms list-keys 1>/dev/null
    log_error 'Failed to get keys list by `aws kms list-keys`.'
  fi
}

# check_key_id(): verify if key id is valid/exist in KMS
function check_key_id() {
  check_key_id_format

  local aws_json="$(get_keys_list)"
  local q_keyAlias='select(.AliasName=="'${kmskey_name}'")'
  local q_keyAliasArn='select(.AliasArn=="'${kmskey_name}'")'
  local q_keyArn='select(.KeyArn=="'${kmskey_name}'")'
  local q_keyId='select(.KeyId=="'${kmskey_name}'")'
  local key_info=""

  for q in "${q_keyAlias}" "${q_keyAliasArn}" "${q_keyArn}" "${q_keyId}"; do
    local key_info="$(echo "${aws_json}" | jq -r ".Keys[]|${q}" 2>/dev/null)"
    if [[ "${key_info}" != "" ]]; then
      key_info="${key_info}"
      break
    fi
  done

  if [[ "${key_info}" == "" ]]; then
    log_error "Cannot find KMS Key by id/arn/alias: ${key_name}"
  fi
}

# check_key_id_format(): check key id/name format
function check_key_id_format() {
  if [[ "${kmskey_name}" =~ ([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]+) ]]; then
    log_debug "Using KeyId: ${kmskey_name}"
  elif [[ "${kmskey_name}" =~ (arn:aws:kms:(.+?):([0-9]+):(key/[a-z0-9\-]+)) ]]; then
    log_debug "Using KeyArn: ${kmskey_name}"
  elif [[ "${kmskey_name}" =~ (arn:aws:kms:(.+?):([0-9]+):(alias/.+)) ]]; then
    log_debug "Using AliasArn: ${kmskey_name}"
  else
    if [[ ! "${kmskey_name}" =~ (^[a-zA-Z0-9:/_-]+$) ]]; then
      log_error "Invalid KMS Key AliasName: ${kmskey_name}"
    elif [[ ! "${kmskey_name}" =~ (alias/(.+)) ]]; then
      kmskey_name="alias/${kmskey_name}"
    fi
    log_debug "Using Alias: ${kmskey_name}"
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

function decrypt_ciphertext() {
  if [[ "$1" == "" ]]; then return; fi

  local aws_cli="aws kms decrypt"
  local aws_arg="--output json --ciphertext-blob"
  local aws_cmd="${aws_cli} ${aws_arg}"
  local decoded="$(echo $1|base64 --decode)"
  local cmd_out="$(${aws_cmd} fileb://<(echo $1|base64 --decode))"
  local decrypt="$(echo "${cmd_out}"|jq -r '.Plaintext'|base64 --decode)"
  local key_arn="$(echo "${cmd_out}"|jq -r '.KeyId')"

  if [[ "${DEBUG}" == "1" ]]; then
    log_debug "Decrypted data -"
    echo "......................................................................."
    echo "${cmd_out}" | jq -r .
    echo "......................................................................."
  fi

  if [[ "$2" != "" ]] && [[ "$2" != "${decrypt}" ]]; then
    echo ""
    log_debug "Comparing original and decrypted text -"
    echo "......................................................................."
    echo "plaintext: $2"
    echo "decrypted: ${decrypt}"
    echo "......................................................................."
    log_error "Decrypted text does not match to original"
  fi

  if [[ "${DEBUG}" == "1" ]]; then
    log_debug "Decrypted text ="
  fi
  echo "${decrypt}"
}

# encrypt(): using
function encrypt() {
  if [[ "$1" == "" ]]; then return; fi

  if [[ "${DEBUG}" == "1" ]]; then
    check_key_id
  else
    check_key_id  1 > /dev/null  # turn off logging to purify stdout
  fi

  local aws_cli="aws kms encrypt"
  local aws_arg="--key-id ${kmskey_name} --plaintext"
  local aws_cmd="${aws_cli} ${aws_arg}"
  local cmd_out="$(${aws_cmd} "$1" 2>/dev/null)"
  local encrypt="$(echo "${cmd_out}" | jq -r .CiphertextBlob 2>/dev/null)"

  if [[ "${cmd_out}" == "" ]]; then
    ${aws_cmd} "$1"
    log_error "Failed to encrypt '$1'"
  elif [[ "${encrypt}" == "" ]]; then
    echo "${cmd_out}" | jq -r .CiphertextBlob
    log_error "Cannot get CiphertextBlob for '$1'"
  elif [[ "${DEBUG}" == "1" ]]; then
    echo "......................................................................."
    echo "${cmd_out}"
    echo "......................................................................."
    decrypt_ciphertext "${encrypt}" "$1"
  else
    echo "${encrypt}"
  fi
}

# get_keys_list(): get a list of KMS keys with id, arn, and alias
function get_keys_list() {
  spaces_json="            "  # 3*4=12 spaces for json indent
  while IFS='\n' read -r line; do
    if [[ "${line}" =~ (\"KeyId\": \"([0-9a-z\-]+)\") ]]; then
      local key_id="${BASH_REMATCH[2]}"
      local select_query='select(.TargetKeyId=="'${key_id}'")'
      local name_query=".Aliases[]|${select_query}|.AliasName"
      local arn_query=".Aliases[]|${select_query}|.AliasArn"
      local key_name="$(echo "${kalias_list}" | jq -r "${name_query}" 2>/dev/null)"
      local key_arn="$(echo "${kalias_list}" | jq -r "${arn_query}" 2>/dev/null)"

      if [[ "${key_name}" != "" ]]; then
        echo "${spaces_json}\"AliasName\": \"${key_name}\","
      fi
      if [[ "${key_arn}" != "" ]]; then
        echo "${spaces_json}\"AliasArn\": \"${key_arn}\","
      fi
    fi
    echo -e "${line}"
  done <<< "${kmskey_list}"
}

# list_keys(): display a list of KMS keys with id, arn, and alias
function list_keys() {
  kmskey_name="${1}"
  kmskey_json="$(get_keys_list)"
  kmskey_list="${kmskey_json}"

  if [[ "${kmskey_name}" != "" ]]; then
    check_key_id_format  # normalize to a valid key

    local q_keyAlias='select(.AliasName|tostring|contains("'${kmskey_name}'"))'
    local q_keyAliasArn='select(.AliasArn|tostring|contains("'${kmskey_name}'"))'
    local q_keyArn='select(.KeyArn|tostring|contains("'${kmskey_name}'"))'
    local q_keyId='select(.KeyId|tostring|contains("'${kmskey_name}'"))'

    for q in "${q_keyAlias}" "${q_keyAliasArn}" "${q_keyArn}" "${q_keyId}"; do
      local key_info="$(echo "${kmskey_json}" | jq -r ".Keys[]|${q}" 2>/dev/null)"
      if [[ "${key_info}" != "" ]]; then
        kmskey_list="${key_info}"
        break
      fi
    done
  fi

  echo "......................................................................."
  echo "${kmskey_list}"
  echo "......................................................................."
}

# log_debug() func: print message as debug warning
function log_debug() {
  set +u
  if [[ "${DEBUG}" == "1" ]]; then
    log_trace "$1" "${2:-DEBUG}"
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


set +u
[[ "$1=None" == "=None" ]] && usage && exit
set -u

[[ $0 != "${BASH_SOURCE}" ]] || main "$@"

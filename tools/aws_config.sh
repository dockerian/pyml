#!/usr/bin/env bash
#######################################################################
# Load/set AWS CLI profile
#
# Command line arguments:
#   $1: aws profile name (the section name in ~/.aws/credentials)
#   $2: --save (optional) to save config (e.g. from env vars)
#
# Dependencies:
#   - AWS CLI command and following config files (content as example)
#   ~/.aws/config
#     [default]
#     output = json
#     region = us-west-2
#     s3_bucket = cyber-intel
#     [profile account1]
#     region = us-west-2
#     [profile account2]
#     region = us-east-1
#
#   ~/.aws/credentials
#     [default]
#     aws_access_key_id = ABCDEFGHIJKLMNOPQRST
#     aws_secret_access_key = AbCdEfGhI/KlMnOpQrStUvWxYz01234567890AbC
#     [account1]
#     aws_access_key_id = ABCDEFGHIJKLMNOPQRST
#     aws_secret_access_key = AbCdEfGhI/KlMnOpQrStUvWxYz01234567890AbC
#     [account2]
#     aws_access_key_id = ABCDEFGHIJKLMNOPQXYZ
#     aws_secret_access_key = AbCdEfGhI/KlMnOpQrStUvWxYz01234567890XyZ
#
#######################################################################
script_file="$( readlink "${BASH_SOURCE[0]}" 2>/dev/null || echo ${BASH_SOURCE[0]} )"
script_name="${script_file##*/}"
script_base="$( cd "$( echo "${script_file%/*}/.." )" && pwd )"
script_path="$( cd "$( echo "${script_file%/*}" )" && pwd )"
config_save=0

# main entry point of the script
function main() {
  shopt -s nocasematch
  for arg in $@ ; do
    if [[ "${arg}" =~ (help|/h|-\?|\/\?) ]] || [[ "${arg}" == "-h" ]]; then
      usage; return
    fi
  done
  # such regex search prevents from any other argument starts with letter 'h'
  if [[ "$@" =~ (help|-h|/h|-\?|\/\?) ]]; then
    usage; return
  fi

  if [[ "$@" =~ (-debug) ]] || [[ "${DEBUG}" =~ (1|enable|on|true|yes) ]]; then
    echo "DEBUG mode is on."
    DEBUG=1
  fi

  if [[ "$2" =~ save ]]; then
    config_save=1
  fi

  aws_config $@ || return $?

  if [[ "${DEBUG}" == "1" ]]; then
    show_env
  fi

  clear_env
}

# aws_config function: load AWS CLI profile and set environment variables
function aws_config() {
  local profile=${1:-default}
  local profile_arg="$([[ "${profile}" != "" ]] && echo "profile.${profile}.")"
  local profile_opt="$([[ "${profile}" != "" ]] && echo "--profile ${profile}")"
  local aws_access_key_id="$(aws configure get aws_access_key_id ${profile_opt} 2>/dev/null)"
  local aws_secret_access_key="$(aws configure get aws_secret_access_key ${profile_opt} 2>/dev/null)"
  local aws_default_region="$(aws configure get ${profile_arg}region 2>/dev/null)"
  local aws_s3_bucket="$(aws configure get ${profile_arg}s3_bucket 2>/dev/null)"

  echo "Loading/Setting AWS CLI profile: ${profile} ..."

  if [[ "${aws_access_key_id}" == "" ]]; then
    if [[ "${AWS_ACCESS_KEY_ID}" == "" ]]; then
      echo "ERROR: Environment variable AWS_ACCESS_KEY_ID is not set."
      return 1
    elif [[ "${#AWS_ACCESS_KEY_ID}" -gt 16 ]]; then
      echo "- using environment variable AWS_ACCESS_KEY_ID"
    else
      echo "ERROR: Wrong size of AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}"
      return 1
    fi
  elif [[ "${#aws_access_key_id}" -gt 16 ]]; then
    echo "- setting environment variable AWS_ACCESS_KEY_ID"
    export AWS_ACCESS_KEY_ID="${aws_access_key_id}"
  else
    echo "ERROR: Wrong size of aws access key id: ${aws_access_key_id}"
    return 1
  fi

  if [[ "${aws_secret_access_key}" == "" ]]; then
    if [[ "${AWS_SECRET_ACCESS_KEY}" == "" ]]; then
      echo "ERROR: Environment variable AWS_SECRET_ACCESS_KEY is not set."
      return 2
    elif [[ "${#AWS_SECRET_ACCESS_KEY}" -eq 40 ]]; then
      echo "- using environment variable AWS_SECRET_ACCESS_KEY"
    else
      echo "ERROR: Wrong size of AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
      return 2
    fi
  elif [[ "${#aws_secret_access_key}" -eq 40 ]]; then
    echo "- setting environment variable AWS_SECRET_ACCESS_KEY"
    export AWS_SECRET_ACCESS_KEY="${aws_secret_access_key}"
  else
    echo "ERROR: Wrong size of aws secret access key: ${aws_secret_access_key}"
    return 2
  fi

  if [[ "${aws_default_region}" == "" ]]; then
    if [[ "${AWS_DEFAULT_REGION}" == "" ]]; then
      echo "ERROR: Environment variable AWS_DEFAULT_REGION is not set."
      return 3
    else
      echo "- using environment variable AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}"
    fi
  else
    echo "- setting environment variable AWS_DEFAULT_REGION=${aws_default_region}"
    export AWS_DEFAULT_REGION="${aws_default_region}"
  fi

  if [[ "${aws_s3_bucket}" != "" ]] && [[ "${S3_BUCKET}" == "" ]]; then
    if [[ "${config_save}" == "1" ]]; then
      aws configure set default.s3_bucket ${aws_s3_bucket}
    fi
    echo "- setting environment variable S3_BUCKET=${aws_s3_bucket}"
    export S3_BUCKET="${aws_s3_bucket}"
  fi

  if [[ "${config_save}" == "1" ]]; then
    echo ""
    echo "- saving AWS_ACCESS_KEY_ID to ${profile} profile"
    aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID} ${profile_opt}

    echo "- saving AWS_SECRET_ACCESS_KEY to ${profile} profile"
    aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY} ${profile_opt}

    echo "- saving config settings to ${profile} profile ..."
    aws configure set ${profile_arg}output json
    aws configure set ${profile_arg}region ${AWS_DEFAULT_REGION}
    aws configure set ${profile_arg}s3_bucket ${S3_BUCKET}
  fi
}

function clear_env() {
  unset DEBUG
  unset script_file
  unset script_base
  unset script_path
  unset config_save
}

function show_env() {
  echo "------------------------------------------------------------"
  echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}"
  echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
  echo "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}"
  echo "------------------------------------------------------------"
}

# usage() func: show help
function usage() {
  echo ""
  echo "USAGE: source ${script_file} profile [--save] [--help]"
  echo ""
  local headers="0"
  # echo "$(cat ${script_path} | grep -e '^##')"
  while IFS='' read -r line || [[ -n "${line}" ]]; do
    if [[ "${headers}" == "0" ]] && [[ "${line}" =~ ^#[#=-\*]{59} ]]; then
      headers="1"
      echo "${line}"
    elif [[ "${headers}" == "1" ]] && [[ "${line}" =~ ^#[#=-\*]{59} ]]; then
      headers="0"
      echo "${line}"
    elif [[ "${headers}" == "1" ]]; then
      echo "${line}"
    fi
  done < "${script_path}"
  echo ""
  clear_env
}

if [[ "$0" == "${BASH_SOURCE}" ]]; then
  usage
  echo "!! Please source this script in order to export envirnment variables !!"
  exit 9
else
  main $@
fi

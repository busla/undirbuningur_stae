#!/bin/bash
set -e

function build() {
  local PROJECT="$1"
  source .venv/bin/activate
  sphinx-build -c projects/"$PROJECT"/ projects/"$PROJECT"/ artifacts/"$PROJECT"_build
  ls -al artifacts
}
function check_diff() {
  local SUBDIR="$1"
  if git diff HEAD^ HEAD --exit-code "SUBDIR" >/dev/null 2>&1
  then
    echo "No changes found in $SUBDIR"
  else
    echo "Changes found in $SUBDIR"
    echo "::set-output name=is-modified::true"
  fi
}

opt=$1
case $opt in
    check_diff) check_diff "${@:2}" ;;
    build) build "${@:2}";;
    *) echo "Nothing to do"
       exit ;;
esac

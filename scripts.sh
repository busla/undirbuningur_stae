#!/bin/bash
declare -a projects=("foundation" "analysis_1")

changed=$(git diff --name-only HEAD^ HEAD)
echo $changed | sed 's/.*\(action\).*/\1/'

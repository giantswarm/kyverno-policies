#!/bin/bash
set -euo pipefail

placeholder="üüü"
# shellcheck disable=SC2016
open_brackets_escaped='{{ `{{` }}'
# shellcheck disable=SC2016
close_brackets_escaped='{{ `}}` }}'

replace () {
  local filename=$1
  local from=$2
  local to=$3
  sed -i.bak "s/$from/$to/g" "$filename" && rm "$filename".bak # https://stackoverflow.com/a/44877280
}

replace_all () {
  local filename=$1
  replace "$filename" '{{' $placeholder
  replace "$filename" '}}' "$close_brackets_escaped"
  replace "$filename" $placeholder "$open_brackets_escaped"
  replace "$filename" '\[\[' '{{'
  replace "$filename" '\]\]' '}}'
}

for i in aws azure common vmware; do
  mkdir -p helm/policies-$i/templates

  cp -a policies/$i/. helm/policies-$i/templates

  # based on https://github.com/koalaman/shellcheck/wiki/SC2044
  while IFS= read -r -d '' filename
  do
    replace_all "$filename"
  done <   <(find helm/policies-"$i"/templates -name '*.yaml' -print0)
done

#!/bin/bash
set -euo pipefail

for i in aws azure common vmware; do
  mkdir -p helm/policies-$i/templates

  cp -a policies/$i/. helm/policies-$i/templates

  for filename in $(find "helm/policies-$i/templates" -name "*.yaml"); do
    echo $filename
    if [[ $(basename $filename) == "Pod.yaml" ]]; then
      echo "skip"
      continue
    fi
    sed -i '' 's/{{/üüü/g' $filename # replace {{ with placeholder
    sed -i '' 's/}}/{{ `}}` }}/g' $filename # replace }} with correct helm substitution
    sed -i '' 's/üüü/{{ `{{` }}/g' $filename # replace the placeholder correct helm substition for {{
  done

done

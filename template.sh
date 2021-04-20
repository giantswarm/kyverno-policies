#!/bin/bash
set -euo pipefail

for i in aws azure common vmware; do
  mkdir -p helm/policies-$i/templates

  cp -a policies/$i/. helm/policies-$i/templates

  for filename in helm/policies-$i/templates/*.yaml; do
    sed -i 's/{{/üüü/g' $filename # replace {{ with placeholder
    sed -i 's/}}/{{ `}}` }}/g' $filename # replace }} with correct helm substitution
    sed -i 's/üüü/{{ `{{` }}/g' $filename # replace the placeholder correct helm substition for {{
  done

done

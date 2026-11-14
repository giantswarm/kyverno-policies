{{- define "debugAccessPolicies.validate" -}}
{{- $policies := .Values.debugAccessPolicies.policies -}}
{{- $blockEnabled := and (hasKey $policies "block-expired-exceptions") (get $policies "block-expired-exceptions").enabled -}}
{{- $purgeEnabled := and (hasKey $policies "purge-expired-exceptions") (get $policies "purge-expired-exceptions").enabled -}}
{{- if and $blockEnabled (not $purgeEnabled) -}}
  {{- fail "debugAccessPolicies: 'block-expired-exceptions' is enabled but 'purge-expired-exceptions' is not. These policies must be co-enabled to ensure expired PolicyExceptions are both blocked at admission and cleaned up on schedule." -}}
{{- end -}}
{{- if and $purgeEnabled (not $blockEnabled) -}}
  {{- fail "debugAccessPolicies: 'purge-expired-exceptions' is enabled but 'block-expired-exceptions' is not. These policies must be co-enabled to ensure expired PolicyExceptions are both blocked at admission and cleaned up on schedule." -}}
{{- end -}}
{{- end -}}

{{/*
debugAccessPolicies.rfc3339Regex is the expiry annotation format check shared by the CEL
policies, written for a CEL single-quoted string literal (backslashes doubled).
*/}}
{{- define "debugAccessPolicies.rfc3339Regex" -}}
^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$
{{- end -}}

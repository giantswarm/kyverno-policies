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

{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "labels.selector" -}}
app.kubernetes.io/name: {{ include "name" . | quote }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "labels.common" -}}
{{ include "labels.selector" . }}
app.kubernetes.io/component: kyverno-policies
app.kubernetes.io/managed-by: {{ .Release.Service | quote }}
app.kubernetes.io/part-of: {{ template "name" . }}
app.kubernetes.io/version: "{{ .Chart.Version | replace "+" "_" }}"
application.giantswarm.io/team: {{ index .Chart.Annotations "io.giantswarm.application.team" | default "shield" | quote }}
helm.sh/chart: {{ include "chart" . | quote }}
{{- if .Values.customLabels }}
{{ toYaml .Values.customLabels }}
{{- end }}
{{- end -}}

{{/*
globToRegex converts a simple glob pattern to a regex pattern for use inside
a CEL string literal. Dots are escaped and '*' becomes '.*'. The pattern is
anchored with ^ and $. Backslashes are doubled for CEL string escaping.

Example: "busybox:*"           -> "^busybox:.*$"
         "registry.io/app:1.*" -> "^registry\\.io/app:1\\..*$"
*/}}
{{- define "globToRegex" -}}
{{- $s := replace "." "\\\\." . -}}
{{- $s = replace "*" ".*" $s -}}
{{- printf "^%s$" $s -}}
{{- end -}}

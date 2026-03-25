# restrict-debug-access policies

The resources in this folder support conditional debug access for "break-glass" or risk-accepted use cases, while generally denying direct shell access.

## Usage

These resources should be used in combination with RBAC limiting the users who are permitted to use `kubectl exec` and `kubectl debug`.

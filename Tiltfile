# Install kyverno from upstream
load('ext://helm_remote', 'helm_remote')
helm_remote(chart='kyverno', repo_url='https://kyverno.github.io/kyverno/', namespace='kyverno', create_namespace=True)

local_resource('generate-helm-chart', 'make generate', deps=['policies'], labels=['generate-policies'])
k8s_yaml(helm('./helm/policies-common'))

# Add task to create a CR and see the mutated result.
template_list = [ item for item in listdir("./e2e") ]
template_list = [ template for template in template_list if os.path.basename(template).endswith("yaml") ]
for template in template_list:
    local_resource(
        name = os.path.basename(template),
        cmd = "kubectl --context {} delete --ignore-not-found=true -f {} && kubectl --context {} apply -f {} && kubectl --context {} get -f {} -o yaml".format(k8s_context(), template, k8s_context(), template, k8s_context(), template),
        auto_init = False,
        trigger_mode = TRIGGER_MODE_MANUAL,
        labels = [ "e2e" ]
    )

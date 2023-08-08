from kubernetes import client
from kubernetes.client.rest import ApiException

def print_resource_list(resources, resource_type):
    print(f"{resource_type.capitalize()}s: {[res.metadata.name for res in resources]}")

def check_resource_privileged_access(resource):
    return any('privileged' in rule.resources and 'get' in rule.verbs for rule in resource.rules)

def get_resource_list(api, namespace, resource_type):
    try:
        resources = api.list_namespaced_resource(resource_type, namespace)
        return resources.items
    except ApiException as e:
        raise Exception(f"Failed to list {resource_type} in {namespace} namespace: " + str(e))

from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Function to set up Kubernetes API client
def setup_kubernetes_client():
    try:
        config.load_kube_config()
        return client.CoreV1Api()
    except Exception as e:
        raise Exception("Failed to set up Kubernetes client: " + str(e))

# Function to list all Kubernetes namespaces
def list_namespaces(api):
    try:
        namespaces = api.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]
    except ApiException as e:
        raise Exception("Failed to list namespaces: " + str(e))

# Function to list all resources in a namespace
def list_resources(api, namespace, resource_type):
    try:
        resources = api.list_namespaced_resource(resource_type, namespace)
        return [res.metadata.name for res in resources.items]
    except ApiException as e:
        raise Exception(f"Failed to list {resource_type} in {namespace} namespace: " + str(e))

# Function to check for privileged access in roles and cluster roles
def check_privileged_access(api, namespace):
    try:
        privileged_access = []
        roles = api.list_namespaced_role(namespace)
        for role in roles.items:
            for rule in role.rules:
                if 'privileged' in rule.resources and 'get' in rule.verbs:
                    privileged_access.append(role.metadata.name)
        cluster_roles = api.list_cluster_role()
        for cluster_role in cluster_roles.items:
            for rule in cluster_role.rules:
                if 'privileged' in rule.resources and 'get' in rule.verbs:
                    privileged_access.append(cluster_role.metadata.name)
        return privileged_access
    except ApiException as e:
        raise Exception(f"Failed to check privileged access in {namespace} namespace: " + str(e))

# Function to check for excessive permissions in roles and cluster roles
def check_excessive_permissions(api, namespace):
    try:
        excessive_permissions = []
        roles = api.list_namespaced_role(namespace)
        for role in roles.items:
            if len(role.rules) > 10:
                excessive_permissions.append(role.metadata.name)
        cluster_roles = api.list_cluster_role()
        for cluster_role in cluster_roles.items:
            if len(cluster_role.rules) > 10:
                excessive_permissions.append(cluster_role.metadata.name)
        return excessive_permissions
    except ApiException as e:
        raise Exception(f"Failed to check excessive permissions in {namespace} namespace: " + str(e))

# Main function
def main():
    try:
        api = setup_kubernetes_client()

        # List all namespaces
        namespaces = list_namespaces(api)

        # Analyze each namespace
        for namespace in namespaces:
            print(f"\nNamespace: {namespace}")

            # List secrets
            secrets = list_resources(api, namespace, 'secret')
            print(f"Secrets: {secrets}")

            # List service accounts
            service_accounts = list_resources(api, namespace, 'service_account')
            print(f"Service Accounts: {service_accounts}")

            # List roles
            roles = list_resources(api, namespace, 'role')
            print(f"Roles: {roles}")

            # Check for privileged access
            privileged_access = check_privileged_access(api, namespace)
            print(f"Privileged Access: {privileged_access}")

            # Check for excessive permissions
            excessive_permissions = check_excessive_permissions(api, namespace)
            print(f"Excessive Permissions: {excessive_permissions}")

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()

# Required libraries
from kubernetes import client, config

# Function to set up Kubernetes API client
def setup_kubernetes_client():
    try:
        # Load Kubernetes configuration from default location or kubeconfig file
        config.load_kube_config()
        return client.CoreV1Api()
    except Exception as e:
        raise Exception("Failed to set up Kubernetes client: " + str(e))

# Function to list all Kubernetes namespaces
def list_namespaces(api):
    try:
        namespaces = api.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]
    except Exception as e:
        raise Exception("Failed to list namespaces: " + str(e))

# Function to list all secrets in a namespace
def list_secrets(api, namespace):
    try:
        secrets = api.list_namespaced_secret(namespace)
        return [secret.metadata.name for secret in secrets.items]
    except Exception as e:
        raise Exception(f"Failed to list secrets in {namespace} namespace: " + str(e))

# Function to list all service accounts in a namespace
def list_service_accounts(api, namespace):
    try:
        service_accounts = api.list_namespaced_service_account(namespace)
        return [sa.metadata.name for sa in service_accounts.items]
    except Exception as e:
        raise Exception(f"Failed to list service accounts in {namespace} namespace: " + str(e))

# Function to list all roles in a namespace
def list_roles(api, namespace):
    try:
        roles = api.list_namespaced_role(namespace)
        return [role.metadata.name for role in roles.items]
    except Exception as e:
        raise Exception(f"Failed to list roles in {namespace} namespace: " + str(e))

# Function to list all cluster roles
def list_cluster_roles(api):
    try:
        cluster_roles = api.list_cluster_role()
        return [cr.metadata.name for cr in cluster_roles.items]
    except Exception as e:
        raise Exception("Failed to list cluster roles: " + str(e))

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
    except Exception as e:
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
    except Exception as e:
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
            secrets = list_secrets(api, namespace)
            print(f"Secrets: {secrets}")

            # List service accounts
            service_accounts = list_service_accounts(api, namespace)
            print(f"Service Accounts: {service_accounts}")

            # List roles
            roles = list_roles(api, namespace)
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

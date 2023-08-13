def list_roles(api, namespace):
    try:
        roles = api.list_namespaced_role(namespace)
        cluster_roles = api.list_cluster_role()
        all_roles = [role.metadata.name for role in roles.items]
        all_cluster_roles = [cluster_role.metadata.name for cluster_role in cluster_roles.items]
        return all_roles + all_cluster_roles
    except ApiException as e:
        raise Exception(f"Failed to list roles in {namespace} namespace: " + str(e))

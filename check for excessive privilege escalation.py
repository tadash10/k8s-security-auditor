def check_privilege_escalation(api, namespace):
    try:
        privilege_escalation_warnings = []
        pods = list_resources(api, namespace, 'pod')
        for pod in pods:
            pod_info = api.read_namespaced_pod(pod, namespace)
            if pod_info.spec.security_context is not None and \
               pod_info.spec.security_context.allow_privilege_escalation:
                privilege_escalation_warnings.append(pod)
        return privilege_escalation_warnings
    except ApiException as e:
        raise Exception(f"Failed to check privilege escalation in {namespace} namespace: " + str(e))

def check_insecure_service_accounts(api, namespace):
    try:
        insecure_service_accounts = []
        service_accounts = list_resources(api, namespace, 'service_account')
        for sa in service_accounts:
            if sa != "default":  # Exclude the default service account
                pods_using_sa = list_resources(api, namespace, 'pod', field_selector=f"spec.serviceAccountName={sa}")
                if not pods_using_sa:
                    insecure_service_accounts.append(sa)
        return insecure_service_accounts
    except ApiException as e:
        raise Exception(f"Failed to check insecure service accounts in {namespace} namespace: " + str(e))

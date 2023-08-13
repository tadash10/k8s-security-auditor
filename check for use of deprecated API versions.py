def check_deprecated_api_versions(api):
    try:
        deprecated_api_warnings = []
        api_versions = api.get_api_versions().versions
        for version in api_versions:
            if "beta" in version or "alpha" in version:
                deprecated_api_warnings.append(version)
        return deprecated_api_warnings
    except ApiException as e:
        raise Exception(f"Failed to check deprecated API versions: " + str(e))

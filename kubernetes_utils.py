from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_api_instance():
    try:
        config.load_kube_config()
        return client.CoreV1Api()
    except Exception as e:
        raise Exception("Failed to set up Kubernetes client: " + str(e))

"""
K8s operator to change deployment specs
"""

from kubernetes import client, config

config.load_kube_config()
v1 = client.AppsV1Api()

def get_fibonacci_deployment()



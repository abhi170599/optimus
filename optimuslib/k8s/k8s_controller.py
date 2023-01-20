"""
K8s operator to change deployment specs
"""

from kubernetes import client, config

config.load_kube_config()
v1 = client.AppsV1Api()

def get_fibonacci_deployment():
    """
    Get the kubernetes deployment of the benchmark app
    """
    all_deployments = v1.list_namespaced_deployment(namespace='default')
    bench_deployment = None
    for deployment in all_deployments.items:
        if deployment.metadata.name=='httpd-deployment-nautilus':
           bench_deployment = deployment
           break
    return bench_deployment

def update_deployment_spec(deployment, resource_spec) -> None:
    """
    Update the resource configs for the deployment
    """
    cpu_req = resource_spec["cpu_req"]
    cpu_lim = resource_spec["cpu_lim"]
    mem_req = resource_spec["mem_req"]
    mem_lim = resource_spec["mem_lim"]
    replicas = resource_spec["replicas"]

    deployment.spec.template.spec.containers[0].resources.requests = {'cpu':f"{cpu_req}m",'memory': f"{mem_req}Mi"}
    deployment.spec.template.spec.containers[0].resources.limits = {'cpu':f"{cpu_lim}m",'memory':f"{mem_lim}Mi"}
    
    deployment.spec.replicas = replicas

    v1.patch_namespaced_deployment(name=deployment.metadata.name,namespace='default',body=deployment)

def is_deployment_ready() -> bool:

    deployment = get_fibonacci_deployment()
    return deployment.status.available_replicas == deployment.status.replicas  

solution=[200, 300, 150, 200, 1]
resource_spec = {
            "cpu_req": solution[0],
            "cpu_lim": solution[1],
            "mem_req": solution[2],
            "mem_lim": solution[3],
            "replicas": solution[4]
        }
deployment = get_fibonacci_deployment()
update_deployment_spec(deployment, resource_spec)

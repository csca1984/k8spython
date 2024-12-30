######
##docker run -d --name k8s-python-nodes -v $HOME/python/kubernetes:/app -v $HOME/.kube/config:/root/.kube/config k8s-python:1.0
#docker run -d --name k8s-python-nodes -v /home/carlos/python/kubernetes:/app -v /home/carlos/python/kubernetes/.kube/config:/root/.kube/config k8s-python:1.0
#docker run -d --name k8s-python-nodes -v /home/carlos/python/kubernetes:/app k8s-python:1.0

#docker run -d --name k8s-python-nodes -v /home/carlos/python/kubernetes:/app k8s-python:1.0 tail -f /dev/null

######

from kubernetes import client, config

def list_kubernetes_clusters():
    # Cargar la configuración de kubeconfig
    contexts, active_context = config.list_kube_config_contexts()
    
    if not contexts:
        print("No se encontraron clústeres de Kubernetes en el archivo kubeconfig.")
        return
    
    print(f"Clúster activo: {active_context['name']}")
    print("Listado de clústeres disponibles:")
    
    for context in contexts:
        print(f"- {context['name']}")

def listar_nodos():
    try:
        # Cargar la configuración del clúster de Kubernetes
        config.load_kube_config()  # Para entorno local, usa este método
        # config.load_incluster_config()  # Si estás corriendo dentro de un pod de Kubernetes

        # Crear una instancia de la API de Kubernetes para interactuar con los nodos
        v1 = client.CoreV1Api()
        
        # Obtener la lista de nodos
        nodos = v1.list_node()

        # Imprimir la lista de nodos
        for nodo in nodos.items:
            print(f"Nombre: {nodo.metadata.name}")
            print(f"Estado: {nodo.status.conditions[-1].type}")  # Estado del nodo
            print(f"IP: {nodo.status.addresses[0].address}")  # Dirección IP del nodo
            print("----")
            if nodo.metadata.labels:
                print("Labels:")
                for key, value in nodo.metadata.labels.items():
                    print(f"  {key}: {value}")
            else:
                print("  No tiene labels.")

    except Exception as e:
        print(f"Error al listar los nodos: {e}")

if __name__ == "__main__":
    listar_nodos()
    list_kubernetes_clusters()
    listar_nodos()


def label_nodes(labels):
    # Configuración para acceder al clúster de Kubernetes
    config.load_kube_config()

    # Crear una instancia de la API de Kubernetes
    v1 = client.CoreV1Api()

    # Iterar sobre los nodos y aplicar las etiquetas
    for node, label in labels.items():
        body = {
            "metadata": {
                "labels": label
            }
        }
        try:
            v1.patch_node(node, body)
            print(f"Etiqueta {label} añadida a {node}")
        except client.rest.ApiException as e:
            print(f"Error al etiquetar {node}: {e}")

if __name__ == "__main__":
    # Etiquetas que quieres añadir a los nodos
    node_labels = {
        "kind-worker": {"role": "worker1"},
        "kind-worker": {"subrole": "test2"},
        "kind-worker2": {"role": "worker2"},
        "kind-worker3": {"role": "worker3"}
    }

    list_kubernetes_clusters()
    label_nodes(node_labels)

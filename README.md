# Airflow on Kubernetes with Docker

This project deploys **Apache Airflow** on **Kubernetes** using **Docker** for containerization. It uses the `KubernetesExecutor` to run tasks as Kubernetes pods, with PostgreSQL for metadata storage. Ideal for scalable data pipeline orchestration. (Work in progress. This project will get progressively stronger and bigger over the course of time!)

```mermaid
graph TD
    A[Kubernetes Cluster] --> B[Airflow Webserver]
    A --> C[Airflow Scheduler]
    A --> D[PostgreSQL]
    A --> E[Dynamic Task Pods]
    B --> D
    C --> D
    C --> E
    F[Docker] --> B
    F --> C
    F --> E
    G[ConfigMap] --> B
    G --> C
    H[Persistent Volume] --> C
    H --> E

    subgraph Legend
        direction LR
        L1[Server] --> L2[Database] --> L3[Container] --> L4[Config] --> L5[Storage]
    end

    B -->|UI Access| I[Web Browser]

    %% Annotations for details
    B:::webserver
    C:::scheduler
    D:::database
    E:::taskpods
    F:::docker
    G:::configmap
    H:::pv
    I:::browser

    classDef webserver fill:#bbf,stroke:#333,stroke-width:2px
    classDef scheduler fill:#bbf,stroke:#333,stroke-width:2px
    classDef database fill:#bdf,stroke:#333,stroke-width:2px
    classDef taskpods fill:#bfb,stroke:#333,stroke-width:2px
    classDef docker fill:#fbd,stroke:#333,stroke-width:2px
    classDef configmap fill:#dfd,stroke:#333,stroke-width:2px
    classDef pv fill:#ddf,stroke:#333,stroke-width:2px
    classDef browser fill:#ffb,stroke:#333,stroke-width:2px
    class A fill:#f9f,stroke:#333,stroke-width:2px

    %% Add details as comments or in the README
    %% B: Deployment: airflow-webserver, Port: 8080 (LoadBalancer)
    %% C: Deployment: airflow-scheduler, KubernetesExecutor
    %% D: StatefulSet: airflow-postgres-postgresql, Metadata Storage
    %% E: Spawned by KubernetesExecutor
    %% F: Image: project-1:1.1
    %% G: e.g., airflow-config, Configurations
    %% H: Optional for DAGs/Logs
    %% I: http://localhost:8080
```

## Features
- **Dynamic Scaling**: Tasks run as Kubernetes pods via `KubernetesExecutor`.
- **Containerized**: Custom Airflow Docker image (`my-airflow:1.0`).
- **Persistent Storage**: PostgreSQL database, with optional Persistent Volumes for DAGs/logs.
- **Cloud-Native**: Runs on any Kubernetes cluster (Minikube, GKE, EKS, AKS).

## Prerequisites
- **Tools**: Docker, Kubernetes (`kubectl`), Helm (optional), Python 3.9+.
- **Access**: Kubernetes cluster and container registry (e.g., Docker Hub).
- **Knowledge**: Airflow DAGs, Dockerfiles, Kubernetes basics.

## Project Structure
```plaintext
my-airflow-project/
├── dags/                # Airflow DAGs
│   └── my_dag.py        # Sample DAG
├── docker/              # Docker files
│   ├── Dockerfile       # Airflow image
│   └── requirements.txt # Dependencies
├── kubernetes/          # Kubernetes manifests
│   ├── airflow-deployment.yaml
│   ├── airflow-service.yaml
│   ├── airflow-configmap.yaml
│   └── pod_template.yaml
├── .env                 # Airflow config
└── README.md
```

## Setup
1. **Build Docker Image**:
   ```bash
   cd docker
   docker build -t my-airflow:1.0 .
   docker push <registry>/my-airflow:1.0
   ```

2. **Configure Airflow**:
   Edit `.env`:
   ```text
   AIRFLOW__CORE__EXECUTOR=KubernetesExecutor
   AIRFLOW__KUBERNETES__NAMESPACE=airflow
   AIRFLOW__KUBERNETES__POD_TEMPLATE_FILE=/path/to/pod_template.yaml
   AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
   AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://user:password@airflow-postgres-postgresql:5432/airflow
   ```

3. **Deploy PostgreSQL**:
   ```bash
   kubectl create namespace airflow
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm install airflow-postgres bitnami/postgresql --namespace airflow \
     --set auth.database=airflow \
     --set auth.username=user \
     --set auth.password=password
   ```

4. **Deploy Airflow**:
   ```bash
   kubectl apply -f kubernetes/airflow-configmap.yaml
   kubectl apply -f kubernetes/airflow-deployment.yaml
   kubectl apply -f kubernetes/airflow-service.yaml
   ```

5. **Initialize Airflow**:
   ```bash
   kubectl exec -it <scheduler-pod-name> -n airflow -- airflow db init
   kubectl exec -it <scheduler-pod-name> -n airflow -- airflow users create \
     --username admin --firstname Admin --lastname User --role Admin \
     --email admin@example.com --password admin
   ```

6. **Access Web UI**:
   - Minikube: `minikube service airflow-webserver -n airflow`
   - Cloud: `kubectl get svc airflow-webserver -n airflow` (use external IP:8080)
   - Login: `admin/admin`

## Usage
- **Add DAGs**: Place `.py` files in `dags/`.
- **Monitor**: Use Airflow UI to trigger/monitor DAGs.
- **Logs**: `kubectl logs <pod-name> -n airflow`.

## Troubleshooting
- **DAGs Missing**: Check `AIRFLOW__CORE__DAGS_FOLDER` and DAG file mounts.
- **Pod Crashes**: View logs (`kubectl logs <pod-name> -n airflow`) for errors (e.g., database issues, resource limits).
- **LoadBalancer Pending**: Use `minikube service` (local) or check cloud provider setup (`kubectl describe svc`).

## Best Practices
- **Resources**: Set CPU/memory limits in `airflow-deployment.yaml`.
- **Security**: Use Secrets for credentials.
- **Monitoring**: Add Prometheus/Grafana for metrics.
- **Persistence**: Use Persistent Volumes for DAGs/logs.

## Contributing
Fork, branch, commit, and submit a Pull Request. Follow code style and include tests.

## License
MIT License. See [LICENSE](LICENSE).

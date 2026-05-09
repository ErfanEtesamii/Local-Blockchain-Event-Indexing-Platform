# Local-Blockchain-Event-Indexing-Platform

## Prerequisites

To get started with this project, I made sure the following tools are installed on my local machine:

1. **Docker**: I use Docker to build and run application containers.

   * I installed Docker Desktop from: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) (Windows/Mac)
   * For Linux, followed the official guide: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

2. **kubectl**: I use this CLI tool to interact with my Kubernetes cluster.

   * **Windows (PowerShell):** `winget install Kubernetes.kubectl`
   * **macOS (Homebrew):** `brew install kubectl`
   * **Linux:** `sudo apt install kubectl`

3. **kind (Kubernetes in Docker)**: I use kind to run a local Kubernetes cluster inside Docker.

   * **macOS (Homebrew):** `brew install kind`
   * **Windows:** I downloaded the binary from: [https://kind.sigs.k8s.io/docs/user/quick-start/](https://kind.sigs.k8s.io/docs/user/quick-start/)
   * **Linux:**

     ```bash
     curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
     chmod +x ./kind
     sudo mv ./kind /usr/local/bin/kind
     ```

---

## Verification

After installing everything, I verified my setup with:

```bash
docker --version
kubectl version --client
kind --version
```

---

### Getting Started

To set up the local infrastructure and deploy the services :

#### 1. Start the Local Kubernetes Cluster
Initialize the cluster using `kind`:
```bash
kind create cluster --name local-blockchain
```
Verify the cluster status:
```bash
kubectl get nodes
```

#### 2. Containerize Services
Building the Docker images for the indexer and API services:
```bash
# Build Indexer
docker build -t my-indexer ./apps/indexer

# Build API
docker build -t my-api ./apps/api
```

#### 3. Deploy to Kubernetes
Loading the images into the kind cluster and apply the Kubernetes manifests:
```bash
# Load images into kind
kind load docker-image my-indexer --name local-blockchain
kind load docker-image my-api --name local-blockchain

# Deploy services
kubectl apply -f infra/k8s/base/
```

#### 4. Verification
Checking the status of deployments in Kubernetes:
```bash
kubectl get pods
```
We should see both `indexer-deployment` and `api-deployment` in `Running` status
I also monitoring my cluster with **Lens** 

***


## Current Progress

Today I added PostgreSQL to the Kubernetes cluster by creating a PersistentVolumeClaim, a Deployment, and a Service for the database. During verification, the PostgreSQL pod initially stayed in `Pending` because Kubernetes could not pull the image from Docker Hub due to network instability and an `ImagePullBackOff` error.

To avoid repeated external downloads, I switched to a local-first workflow. I built the API and indexer images locally and successfully loaded them into the `kind` cluster. This confirmed that the local Docker setup and the `kind` cluster are working correctly, and it reduced the need for internet access during deployment.

At this point, the infrastructure includes:
- A running local Kubernetes cluster.
- Locally built API and indexer images loaded into `kind`.
- A PostgreSQL configuration added to the cluster manifests.

The next step is to finalize the Kubernetes manifests for the application services so they run entirely from local images without pulling from the network.
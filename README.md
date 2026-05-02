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

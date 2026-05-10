# Local-Blockchain-Event-Indexing-Platform

## Project Overview

In this project, I am building a local blockchain event indexing platform designed to collect, store, and expose blockchain transfer events through a backend API service.

I built the infrastructure around:

* Kubernetes (`kind`)
* Docker
* PostgreSQL
* Local containerized services

My goal is to create a fully local-first development environment for indexing blockchain events and exposing them through scalable backend services.

---

# Prerequisites

To get started with this project, I installed the following tools on my local machine.

## 1. Docker

I use Docker to build and run the application containers.

### Installation

I installed Docker Desktop from:

```text
https://www.docker.com/products/docker-desktop/
```

---

## 2. kubectl

I use `kubectl` to interact with my Kubernetes cluster.

### Installation

#### Windows (PowerShell)

```bash id="jlwm8w"
winget install Kubernetes.kubectl
```

---

## 3. kind (Kubernetes in Docker)

I use `kind` to run a local Kubernetes cluster inside Docker.

### Installation

#### Windows

I downloaded the binary from:

```text id="lgp8u7"
https://kind.sigs.k8s.io/docs/user/quick-start/
```

---

## 4. PostgreSQL

I use PostgreSQL as the primary relational database for storing indexed blockchain events.

### Database Tools

* I use PostgreSQL as the main database system.
* I use pgAdmin for graphical database management, query execution, and schema inspection.

---

# Environment Verification

After installing the required tools, I verified my setup with:

```bash id="r5clbh"
docker --version
kubectl version --client
kind --version
```

---

# Getting Started

## 1. Create the Local Kubernetes Cluster

I initialize the cluster using `kind`:

```bash id="4zkmli"
kind create cluster --name local-blockchain
```

Then I verify the cluster status:

```bash id="5xtwns"
kubectl get nodes
```

---

## 2. Build the Application Containers

I build the Docker images for the indexer and API services.

### Build Indexer

```bash id="v76udw"
docker build -t my-indexer ./apps/indexer
```

### Build API

```bash id="cbj9y6"
docker build -t my-api ./apps/api
```

---

## 3. Load Images into the kind Cluster

I load the local Docker images into the Kubernetes cluster:

```bash id="3eq36g"
kind load docker-image my-indexer --name local-blockchain
kind load docker-image my-api --name local-blockchain
```

---

## 4. Deploy the Infrastructure

I deploy the Kubernetes manifests using:

```bash id="gdn5g9"
kubectl apply -f infra/k8s/base/
```

---

## 5. Verify Deployments

I check the running pods with:

```bash id="4xj1iu"
kubectl get pods
```

Expected running services:

* `indexer-deployment`
* `api-deployment`
* PostgreSQL deployment

---

# Monitoring

I monitor the Kubernetes cluster locally using Lens.

---

# Database Layer

I configured a PostgreSQL database for storing indexed blockchain transfer events.

## Current Table

### `token_transfers`

Columns:

* `tx_hash`
* `block_number`
* `event_index`
* `from_address`
* `to_address`
* `token_address`
* `amount`
* `status`
* `processed_at`
* `created_at`

---

# Schema Setup

I stored the initial database schema in:

```text id="y8d98m"
infra/db/schema.sql
```

The schema creates:

* the `token_transfers` table,
* indexes on:

  * block number,
  * token address,
  * sender address,
  * receiver address.

---

# Infrastructure Progress

## Completed

So far, I have:

* Defined the project scope and architecture.
* Designed the PostgreSQL database schema.
* Installed and configured PostgreSQL locally.
* Created the `token_transfers` table.
* Executed the schema successfully.
* Verified database connectivity.
* Inserted and validated test records.
* Added PostgreSQL to the Kubernetes cluster.
* Created:

  * a PersistentVolumeClaim,
  * a PostgreSQL Deployment,
  * a PostgreSQL Service.
* Built the API and indexer Docker images locally.
* Loaded local images into the `kind` cluster successfully.
* Verified local Docker and Kubernetes integration.

---

# Issues Encountered

During deployment verification, the PostgreSQL pod initially remained in `Pending` state due to an `ImagePullBackOff` error caused by Docker Hub connectivity issues and network instability.

To avoid repeated external downloads, I switched to a local-first workflow by using locally built Docker images and loading them directly into the `kind` cluster.

This approach:

* reduces internet dependency,
* speeds up deployments,
* improves local development reliability.

---

# Current Infrastructure Status

At this stage, my infrastructure includes:

* A running local Kubernetes cluster.
* PostgreSQL configured inside Kubernetes.
* Local API and indexer images loaded into `kind`.
* Kubernetes manifests for infrastructure deployment.
* A functional PostgreSQL schema for blockchain event storage.

---

## Repository Structure

```text
.
├── README.md
├── infra/
│   ├── db/
│   │   └── schema.sql
│   └── k8s/
│       └── base/
│           ├── namespace.yaml
│           ├── postgres-configmap.yaml
│           ├── postgres-secret.yaml
│           ├── postgres-pv.yaml
│           ├── postgres-pvc.yaml
│           ├── postgres-deployment.yaml
│           ├── postgres-service.yaml
│           ├── api-deployment.yaml
│           ├── api-service.yaml
│           ├── indexer-deployment.yaml
│           ├── indexer-service.yaml
│           ├── ingress.yaml
│           └── kustomization.yaml
├── app/
│   ├── api/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── schemas.py
│   └── indexer/
│       ├── main.py
│       ├── processor.py
│       └── blockchain_client.py
├── scripts/
│   ├── init_db.sql
│   └── seed_test_data.sql
└── docs/
    ├── architecture.md
    └── deployment.md
```

# Next Steps

The next phase of development includes:

* Connecting the backend API service to PostgreSQL.
* Creating the first API endpoint for indexed transfers.
* Finalizing Kubernetes manifests for fully local deployments.
* Running all services entirely from local Docker images.
* Expanding the blockchain event indexing functionality.

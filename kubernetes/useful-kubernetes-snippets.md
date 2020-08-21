# Useful Kubernetes Snippets

## Kubernetes
```bash
kubectl -n <NAMESPACE> describe pod <POD_NAME>
kubectl -n <NAMESPACE> logs <POD_NAME>
kubectl -n <NAMESPACE> get pod <POD_NAME> -o yaml
```

### Containers
```bash
kubectl -n <NAMESPACE> exec -it <CONTAINER_NAME> -- bash
```

### Secrets
```bash
kubectl -n <NAMESPACE> get secret <SECRET_NAME> -o yaml
echo <SECRET> | base64 --decode
```

---

## Helm

```bash
helm init
helm dependency update
helm install .
```

---

## AWS

### ECR
```bash
ECR_PASSWORD=`aws ecr get-login --region us-west-2 --registry-ids <AWS_ACCOUNT_ID> | cut -d' ' -f6`
kubectl create secret docker-registry aws-ecr-registry --docker-server=<AWS_ACCOUNT_ID>.dkr.ecr.us-west-2.amazonaws.com --docker-username=AWS --docker-password=$ECR_PASSWORD --docker-email=<AWS_ACCOUNT_EMAIL>
```

### EKS
```bash
aws eks --region us-west-2 update-kubeconfig --name <CLUSTER_NAME>
```

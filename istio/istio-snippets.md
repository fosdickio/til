# Istio Snippets

## Deployment

Create a namespace where the application would be deployed:

```sh
$ kubectl create namespace my-test-app
```

Enable automatic sidecar injection for the namespace:

```sh
$ kubectl label namespace my-test-app istio-injection=enabled
```

Deploy the application in the namespace created above:

```sh
$ kubectl apply -n my-test-app -f my-test-app-manifests.yaml
```

Ensure that all the pods are in the running state and have the sidecar proxy injected:

```sh
$ kubectl -n my-test-app get pods
```

Verify that the `STATUS` column of all the pods is `Running`. You should also verify that the `READY` column shows `2/2` to indicate that 2 containers are running in every pod; one for the application workload and another for the injected sidecar proxy.

Note that it might take up to a few minutes for all the pods to be in running state, so wait before proceeding to the next verification step.

You can verify that the correct versions of all components (control and data plane) are running in your cluster by using the `istioctl` version command. For example, if version 1.9.1 was installed, you should see the following output:

```sh
$ istioctl version
client version: 1.9.1
control plane version: 1.9.1
data plane version: 1.9.1 (13 proxies)
```

Verify that Istio is installed correctly and all the checks are passing:

```sh
$ istioctl verify-install
```

## Configure Istio Ingress Gateway

Check that the service type of `istio-ingressgateway` is `LoadBalancer`.

```sh
$ kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.type}'
```

You need to be able to access the `istio-ingressgateway` service from outside your cluster. You can check that status of the external IP of the `istio-ingressgateway` service by issuing the following command:

```sh
$ kubectl -n istio-system get svc istio-ingressgateway
```

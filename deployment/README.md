
```powershell

nerdctl build -t test-flask:latest --namespace k8s.io .

k create deployment test-flask --image=nginx --replicas 1 --dry-run=client -o yaml -n test > deployment.yaml

kubectl apply -f system
kubectl apply -f data
kubectl apply -f .

kubectl delete -f data
kubectl delete -f test-flask.yaml

# 
kubectl port-forward svc/test-flask -n test 5000:5000
kubectl port-forward --namespace=kube-system service/traefik 8080:80

```
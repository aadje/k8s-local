
```powershell

# Deploy
kubectl apply -f system
kubectl apply -f data
kubectl apply -f services

# Delete
kubectl delete -f data
kubectl delete -f services\test-flask.yaml

```
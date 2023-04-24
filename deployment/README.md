
```powershell

# Deploy
kubectl apply -f system
kubectl apply -f data
kubectl apply -f .

# Delete
kubectl delete -f data
kubectl delete -f test-flask.yaml

```
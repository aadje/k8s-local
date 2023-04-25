
```powershell

# Deploy
kubectl create namespace cert-manager
kubectl create secret generic azuredns-config -n cert-manager --from-literal="client-secret=$PASSWORD"
kubectl apply -f ./deployment/system/cert-manager

kubectl apply -f ./deployment/system/traefik

kubectl apply -f ./deployment/data

kubectl apply -f ./deployment/services

# Delete
kubectl delete -f ./deployment/data
kubectl delete -f ./deployment/services/test-flask.yaml

```
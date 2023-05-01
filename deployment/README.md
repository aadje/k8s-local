
```powershell

# Deploy
kubectl create secret generic azuredns-config -n kube-system --from-literal="client-secret=$PASSWORD"
code ./deployment/system/cert-manager/acme-issuer.yaml

kubectl apply -f ./deployment/system/sealed-secrets-helm-chart.yaml

kubectl apply -k ./deployment/system/cert-manager
kubectl apply -k ./deployment/system/traefik
kubectl apply -k ./deployment/data
kubectl apply -k ./deployment/services

kubectl apply -f ./deployment/services/test-flask.yaml
kubectl apply -f ./deployment/services/test-django.yaml

# Delete
kubectl delete -f ./deployment/data
kubectl delete -f ./deployment/services/test-flask.yaml

## Delete mysql data and load initdb script
wsl -d rancher-desktop rm -r "/var/lib/mysql"

```
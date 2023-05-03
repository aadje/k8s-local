
```powershell

# Deploy
code ./system/cert-manager/acme-issuer.yaml

kubectl apply -f ./system/sealed-secrets-helm-chart.yaml

## Apply all 
kubectl apply -k .

## Apply groups
kubectl apply -k ./system/cert-manager
kubectl apply -k ./system/traefik
kubectl apply -k ./data
kubectl apply -k ./services

## Apply service
kubectl apply -f ./services/test-flask.yaml
kubectl apply -f ./services/test-django.yaml

# Delete
kubectl delete -f ./data
kubectl delete -f ./services/test-flask.yaml

## Delete mysql data and load initdb script
wsl -d rancher-desktop rm -r "/var/lib/mysql"

## Store lets encrypt cert for debugging
kubectl get secret wildcard-k8slocal-com -n kube-system -o "jsonpath={.data['tls\.crt']}" | base64 -d > ".venv/tls.crt"
kubectl get secret wildcard-k8slocal-com -n kube-system -o "jsonpath={.data['tls\.key']}" | base64 -d > ".venv/tls.key"

```
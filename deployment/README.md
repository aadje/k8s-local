
```sh

# Deploy
## Sealed secrets TLS secret key pair
az keyvault secret download --id "https://$(Read-Host vault name).vault.azure.net/secrets/lcl-sealed-secret" -f "tls.pfx" --encoding base64
(openssl pkcs12 -in tls.pfx -nocerts -nodes -passin pass:"" | openssl rsa) -join "`n" | Set-Content tls.key -NoNewline
(openssl pkcs12 -in tls.pfx -nokeys -clcerts -nodes -passin pass:"" | openssl x509) -join "`n" | Set-Content tls.crt -NoNewline
kubectl create secret tls sealed-secrets-key -n kube-system --key="tls.key" --cert="tls.crt"
kubectl label secret -n kube-system sealed-secrets-key sealedsecrets.bitnami.com/sealed-secrets-key=active

## Update acme-issuer
code ./system/cert-manager/acme-issuer.yaml
git update-index --skip-worktree ./system/cert-manager/acme-issuer.yaml

## Apply all
kubectl apply -k .

## Apply per groups
kubectl apply -f ./system/sealed-secrets-helm-chart.yaml
kubectl apply -k ./system/cert-manager
kubectl apply -k ./system/traefik
kubectl apply -k ./data
kubectl apply -k ./data/kafka
kubectl apply -k ./services

## Apply per services

docker build -t test-flask:latest ../hello_flask
docker build -t test-django:latest ../hello_django
docker build -t test-asp:latest ../hello_asp 

kubectl rollout restart deployment -n dev

kubectl apply -f ./services/test-flask.yaml
kubectl apply -f ./services/test-django.yaml
kubectl apply -f ./services/test-asp.yaml

# Delete
kubectl delete -f ./data
kubectl delete -f ./services/test-flask.yaml

## Delete mysql data and load initdb script
wsl -d rancher-desktop rm -r "/var/lib/mysql"

## Store let's encrypt cert for local debugging
kubectl get secret wildcard-k8slocal-com -n kube-system -o "jsonpath={.data['tls\.crt']}" | base64 -d > ".venv/tls.crt"
kubectl get secret wildcard-k8slocal-com -n kube-system -o "jsonpath={.data['tls\.key']}" | base64 -d > ".venv/tls.key"

## Convert PKCS#1 key to PKCS#8 formatted key with password for ASP
openssl pkcs8 -inform PEM -topk8 -in .venv/tls.key -out .venv/tls-pkcs8.key -passin pass:123 -passout pass:123

# Add Hostsfile entries using hostsfile script from https://gist.github.com/aadje/a906790b4b111c03acd81d07bc446756
hf add traefik,mysql,rabbitmq,redis,elasticsearch6,kafka,kafdrop,redpanda,test-django,test-flask

# Test tcp routes
redis-cli -h redis.k8slocal.com
curl http://elasticsearch6.k8slocal.com:9200
mysql -h mysql.k8slocal.com -u root

```
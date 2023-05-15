
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

docker build -t hello-flask:latest ../hello_flask
docker build -t hello-django:latest ../hello_django
docker build -t hello-asp:latest ../hello_asp 

kubectl rollout restart deployment -n lcl

kubectl apply -f ./services/hello-flask.yaml
kubectl apply -f ./services/hello-django.yaml
kubectl apply -f ./services/hello-asp.yaml

# Delete
kubectl delete -f ./data
kubectl delete -f ./services/hello-flask.yaml

## Delete mysql data and load initdb script
wsl -d rancher-desktop rm -r "/var/lib/mysql"
python manage.py migrate

## Store let's encrypt cert for local debugging
kubectl get secret wildcard-k8slocal-com -n kube-system -o "jsonpath={.data['tls\.crt']}" | base64 -d > "../env/tls.crt"
kubectl get secret wildcard-k8slocal-com -n kube-system -o "jsonpath={.data['tls\.key']}" | base64 -d > "../env/tls.key"

## Convert PKCS#1 key to PKCS#8 formatted key with password for ASP
openssl pkcs8 -inform PEM -topk8 -in ../env/tls.key -out ../env/tls-pkcs8.key -passin pass:123 -passout pass:123

# Add Hostsfile entries using hostsfile script from https://gist.github.com/aadje/a906790b4b111c03acd81d07bc446756
hf add traefik,mysql,rabbitmq,redis,elasticsearch6,kafka,kafdrop,redpanda,hello-django,hello-flask,hello-asp -f

# Test tcp routes
redis-cli -h redis.k8slocal.com
curl http://elasticsearch6.k8slocal.com:9200
mysql -h mysql.k8slocal.com -u root

# Test Apps
## Flask
cd hello_flask/hello_app
poetry shell
$env:FLASK_APP = "webapp"
flask run
flask run --host hello-flask.k8slocal.com --port 80
flask run --host hello-flask.k8slocal.com --port 443 --cert ../../env/tls.crt --key ../../env/tls.key

## Django
cd hello_django
poetry shell
python -m manage runserver_plus
python -m manage runserver_plus hello-django.k8slocal.com:80
python -m manage runserver_plus --cert-file ../env/tls.crt --key-file ../env/tls.key hello-django.k8slocal.com:443

# Trigger new cert
cmctl renew wildcard-k8slocal-com -n kube-system


```
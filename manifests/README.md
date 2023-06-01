
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

## Install portainer
kubectl apply -f ./system/portainer.yaml

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
docker build -t hello-nextjs:latest ../hello_nextjs

kubectl rollout restart deployment -n lcl

kubectl apply -f ./services/hello-flask.yaml
kubectl apply -f ./services/hello-django.yaml
kubectl apply -f ./services/hello-asp.yaml
kubectl apply -f ./services/hello-nextjs.yaml

# Delete
kubectl delete -f ./data
kubectl delete -f ./services/hello-flask.yaml

## Delete mysql data and load initdb script
wsl -d rancher-desktop rm -r "/var/lib/mysql"
python manage.py migrate

# Add Hostsfile entries using hostsfile script from https://gist.github.com/aadje/a906790b4b111c03acd81d07bc446756
hf add traefik,mysql,rabbitmq,redis,elasticsearch6,kafka,kafdrop,redpanda -f
hf add lcl-hello-django,lcl-hello-flask,lcl-hello-asp,lcl-hello-nextjs, dev-hello-django,dev-hello-flask,dev-hello-asp,dev-hello-nextjs -f

# Test tcp routes
redis-cli -h redis.k8slocal.com
curl http://elasticsearch6.k8slocal.com:9200
mysql -h mysql.k8slocal.com -u root

# Test apps
## Asp
cd ../hello_asp
dotnet run
## Django
cd ../hello_django
. ./.venv/Scripts/activate
python -m manage runserver "0.0.0.0:3002"
## Flask 
cd ../hello_flask
. ./.venv/Scripts/activate
cd ./hello_app
$env:FLASK_APP='webapp'
python -m flask run --host '0.0.0.0' --port 3003 --no-debugger
deactivate
## Nextjs
cd ../hello_nextjs
npm run dev

# Trigger Letsencrypt cert rollover
cmctl renew wildcard-k8slocal-com -n kube-system

```
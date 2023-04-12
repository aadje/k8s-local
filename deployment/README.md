
```powershell

k create deployment test-flask --image=nginx --replicas 1 --dry-run=client -o yaml -n test > deployment.yaml

kubectl apply -f test-flask-application.yaml

kubectl port-forward svc/test-flask -n test 5000:5000

```
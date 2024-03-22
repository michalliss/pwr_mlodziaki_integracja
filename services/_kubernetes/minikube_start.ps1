minikube start --memory 4096 --cpus 2

# Start minikube tunnel in the background
$tunnelJob = Start-Job -ScriptBlock { minikube tunnel }

# Wait for the tunnel to successfully start
while ($true) {
    $jobOutput = Receive-Job -Job $tunnelJob -Keep
    if ($jobOutput -match "\* Tunnel successfully started") {
        break
    }
    Start-Sleep -Seconds 1
}

minikube addons enable ingress
minikube dashboard
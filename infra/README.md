The pods will rollout in a few seconds. To check the status:

  kubectl -n redpanda rollout status statefulset redpanda --watch

Set up rpk for access to your external listeners:
  kubectl get secret -n redpanda redpanda-external-cert -o go-template='{{ index .data "ca.crt" | base64decode }}' > ca.crt
  rpk profile create --from-profile <(kubectl get configmap -n redpanda redpanda-rpk -o go-template='{{ .data.profile }}') default

Set up dns to look up the pods on their Kubernetes Nodes. You can use this query to get the list of short-names to IP addresses. Add your external domain to the hostnames and you could test by adding these to your /etc/hosts:

  kubectl get pod -n redpanda -o custom-columns=node:.status.hostIP,name:.metadata.name --no-headers -l app.kubernetes.io/name=redpanda,app.kubernetes.io/component=redpanda-statefulset

Try some sample commands:

Get the api status:

  rpk cluster info

Create a topic

  rpk topic create test-topic -p 3 -r 1

Describe the topic:

  rpk topic describe test-topic

Delete the topic:

  rpk topic delete test-topic

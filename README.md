# Webhook message queue
The webhook message queue is designed to receive webhooks from services (producer) and
store the payload JSON as a dictionary in a redis queue. Any consuming service can make a REST call
to get the list of payloads of the queued webhooks

It is designed to work with a [Webhook Relay](https://github.com/lscsoft/webhook-relay) that
validates and relays webhooks from known services such as DockerHub, Docker
registries, GitHub, and GitLab. However, this is not required and the receiver
may listen directly to these services.

All webhooks must be send to path `/webhook-producer` inorder to queue the webhook.
A producer token must be passed as query param to authenticate.

In order to get the list of webhooks queued in redis. A POST call must be made to `/webhook-consumer`
A consumer token must be passed as query param to authenticate.

Consumer and producer tokens can be set in the docker-compose file

Once the webhooks are requested by the consumer, the webhooks are removed from the queue

## Running

The message queue requires [docker-compose](https://docs.docker.com/compose/install/)
and, in its simplest form, can be invoked with `docker-compose up`. By default,
it will bind to `localhost:8080` but allow clients from all IP addresses. This
may appear odd, but on MacOS and Windows, traffic to the containers will appear
as though it's coming from the gateway of the network created by
Docker's linux virtualization.

In a production environment without the networking restrictions imposed by
MacOS/Windows, you might elect to provide different defaults through the
the shell environment. _e.g._
```
ALLOWED_IPS=A.B.C.D LISTEN_IP=0.0.0.0 docker-compose up
```
where `A.B.C.D` is an IP address (or CIDR range) from which your webhooks will
be sent.


This repo was forked from https://github.com/lscsoft/webhook-queue

# sms-sender service
[MIT License](LICENSE.txt)

Microservice for sending SMS messages.

The project pursues educational and research goals. It can be the base of a real microservice. But I doubt that radis-om is ready for use in production at the moment.

# System Components
```mermaid
flowchart TB
    c(Core - gRPC controller)
    r0[(Redis DB 0 storage)]
    r1[(Redis DB 1 celery backend)]
    rq[\RabbitMQ/]
    cw[[Celery worker]]
    d[[Delivery API]]
    c-->r0
    d-->r0
    cw-->r0
    c-->cw
    cw-->rq
    cw-->r1
    
    
```

# Installation
```shell
git clone https://github.com/edelwi/sms-service.git
cd sms-service
# run service
docker-compose up --build  # build and run containers (console attached mode, add -d to detach)
```

# Run client
```shell
python3  -m venv venv
source ./venv/bin/activate  # activate virtual environment (on linux) on Windows run venv\Scripts\activate.bat
pip install grpcio==1.54.2 requests==2.31.0
python sms_client.py
```

# Interaction schemes

## SMS sending scheme
```mermaid
sequenceDiagram
    participant sms-sender client
    participant Core
    participant Redis
    participant Celery
    participant Provider
    sms-sender client->>+Core: Send SMS (gRPC)
    Core-->>Redis: Store SMS ID 1
    Core-->>Celery: Send SMS ID 1
    Core->>-sms-sender client: Remember ID 1. (gRPC)
    Celery-->>Redis: Give me SMS ID 1.
    Redis-->>Celery: Here you are. SMS ID 1.
    loop until response 200, max_retries=11, retry_backoff=5, retry_jitter=True
        Celery->>+Provider: Deliver SMS ID 1. (HTTP)
    end
    Provider->>-Celery: Ok, see status. (HTTP)
    Celery-->>Redis: Store SMS ID 1 ending status.
    sms-sender client->>+Core: Did you send SMS ID 1? (gRPC)
    Core-->>Redis: Are there any sent SMS ID 1?
    alt is sent
        Redis-->>Core: Ok.
    else is not sent
        Redis-->>Core: No, something wrong :(
    end
    Core->>-sms-sender client: SMS ID 1 sending status.
```

## SMS Delivery schema
```mermaid
sequenceDiagram
    participant sms-sender client
    participant Core
    participant Redis
    participant Celery
    participant Delivery API
    participant Provider
    Note left of Provider: The provider can send a delivery notification within 24 hours.
    sms-sender client->>+Core: Was SMS ID 1 delivered? (gRPC)
    Core-->>Redis: Are there any delivered SMS with ID 1?
    Redis-->Core: No.
    Core->>-sms-sender client: No. (gRPC)
    Note left of Provider: Provider send a delivery notification.
    Provider->>+Delivery API: SMS ID 1 delivery notification.
    Delivery API-->>Redis: Store SMS ID 1 delivery notification.
    Delivery API->>-Provider: Ok.

    sms-sender client->>Core: Was SMS ID 1 delivered? (gRPC)
    Core-->>Redis: Are there any delivered SMS with ID 1?
    Redis-->Core: Yes.
    alt delivered
        Core->>sms-sender client: Yes, delivered to... (gRPC)
    else delivery failed
        Core->>sms-sender client: No, the provider failed to deliver the message. (gRPC)
    end
```


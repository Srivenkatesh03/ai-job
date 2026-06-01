# EVENT_SCHEMA.md

# Event-Driven Architecture Schema

## Overview

The platform uses an event-driven architecture for scalable, asynchronous workflow orchestration.

Events are used to coordinate:

* workflows
* queues
* AI processing
* notifications
* analytics
* automation pipelines

All services must communicate using standardized event contracts.

---

# Event System Goals

## Primary Objectives

* loose coupling
* async workflows
* scalable orchestration
* observability
* replay support
* failure isolation

---

# Event Naming Rules

## Naming Convention

Use:

```plaintext id="evt1001"
resource.action
```

Examples:

```plaintext id="evt1002"
resume.uploaded
resume.optimized
workflow.started
workflow.failed
job.match.completed
notification.sent
```

---

# Event Structure

## Standard Event Schema

```json id="evt1003"
{
  "event_id": "uuid",
  "event_name": "resume.uploaded",
  "event_version": "v1",
  "timestamp": "ISO8601",
  "source": "backend-api",
  "workflow_id": "uuid",
  "user_id": "uuid",
  "payload": {},
  "metadata": {}
}
```

---

# Required Event Fields

| Field         | Description             |
| ------------- | ----------------------- |
| event_id      | unique event identifier |
| event_name    | event type              |
| event_version | schema version          |
| timestamp     | event timestamp         |
| source        | originating service     |
| workflow_id   | workflow correlation    |
| payload       | event data              |

---

# Event Categories

## Workflow Events

```plaintext id="evt1004"
workflow.started
workflow.completed
workflow.failed
workflow.retrying
```

---

## Resume Events

```plaintext id="evt1005"
resume.uploaded
resume.parsed
resume.optimized
resume.scored
```

---

## AI Events

```plaintext id="evt1006"
ai.request.started
ai.request.completed
ai.provider.failed
ai.validation.failed
```

---

## Notification Events

```plaintext id="evt1007"
notification.created
notification.sent
notification.failed
```

---

## Queue Events

```plaintext id="evt1008"
queue.task.started
queue.task.completed
queue.task.failed
```

---

# Event Versioning

## Version Rules

Events must support:

* backward compatibility
* schema evolution
* version tracking

---

# Event Delivery Rules

## Delivery Requirements

Events must support:

* retries
* idempotency
* observability
* failure recovery

---

# Event Idempotency

## Mandatory Rules

Repeated events must NOT cause:

* duplicate notifications
* duplicate DB writes
* repeated AI charges

---

# Event Security

## Security Requirements

* validate payloads
* authenticate producers
* sanitize event data
* encrypt sensitive payloads

---

# Event Observability

## Monitoring Requirements

Track:

* event throughput
* failed events
* retry frequency
* processing latency

---

# Final Goal

The event architecture should resemble:

* enterprise event-driven systems
* scalable workflow orchestration platforms
* cloud-native async infrastructure

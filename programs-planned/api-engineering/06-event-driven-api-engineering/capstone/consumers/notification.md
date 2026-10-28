# Notification consumer

**Inputs:** terminal run facts.

**Effect:** create one durable notification intent. Sending email or another external notification is a second idempotent delivery step, never part of broker acknowledgement.

**Replay:** dry-run by default. An approved new effect version is required before historical events can create new notification intents.

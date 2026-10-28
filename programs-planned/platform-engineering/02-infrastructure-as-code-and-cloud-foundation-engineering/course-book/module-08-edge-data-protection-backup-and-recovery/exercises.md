# Exercises — Edge, Data Protection, Backup, and Recovery

## 1. Request path

Trace the control and data components between a DNS query and an Atlas HTTP response.

## 2. Certificate versus DNS authority

Why should certificate ownership be considered separately from DNS record ownership?

## 3. Overly broad health checks

What is the danger of making an ALB health check depend on every optional downstream service?

## 4. Detection time

Calculate approximate unhealthy detection time for a 15-second interval and three consecutive failures. What else can change the observed time?

## 5. Security-group reference

Why should the Atlas host accept its application port from the ALB security group instead of the VPC CIDR?

## 6. Three storage properties

Distinguish availability, durability, and recoverability with an EBS example.

## 7. Encrypted snapshot limits

Why does an encrypted snapshot not by itself prove recoverability?

## 8. RPO/RTO statement

Define defensible RPO and RTO statements for hourly backups and a 30-minute measured restore.

## 9. Backup manifest

What must a backup manifest contain to support an integrity check?

## 10. Empty restore

Why restore into an empty destination?

## 11. Protection mechanisms

Distinguish deletion protection, versioning, lifecycle retention, and object immutability.

## 12. Public-edge proof

Design a post-apply test that proves the public edge without exposing the private host.

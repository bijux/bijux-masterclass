CREATE TABLE IF NOT EXISTS webhook_subscriptions (
  subscription_id text PRIMARY KEY, tenant_id text NOT NULL, destination text NOT NULL, state text NOT NULL, version bigint NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS webhook_deliveries (
  delivery_id text PRIMARY KEY, subscription_id text NOT NULL REFERENCES webhook_subscriptions(subscription_id),
  event_id text NOT NULL, state text NOT NULL, attempts integer NOT NULL DEFAULT 0, next_attempt_at timestamptz,
  UNIQUE(subscription_id, event_id)
);

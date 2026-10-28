# Consumer implementations and ownership

Each consumer owns one explicit effect. It must validate the event contract, enforce tenant and producer policy, begin a transaction, insert its inbox identity, apply the effect, commit, and only then acknowledge delivery.

The files in this directory describe operational ownership. Executable mechanics live in the Python and TypeScript tracks.

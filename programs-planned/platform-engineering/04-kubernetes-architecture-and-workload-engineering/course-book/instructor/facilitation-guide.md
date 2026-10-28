# Facilitation guide

Do not demonstrate a command before the learner can name the object and owner it queries or mutates. Ask for a prediction before every controlled failure. During review, reject explanations that jump layers—for example, using application logs to explain a Pod that never scheduled.

Use the semantic lane first because it exposes state transitions deterministically. Use kind second to reveal real API defaulting, asynchronous convergence, and runtime behavior. Never let a successful kind experiment be described as production evidence.

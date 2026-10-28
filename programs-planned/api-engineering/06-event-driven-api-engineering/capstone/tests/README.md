# Capstone proof ownership

Executable tests are colocated with each implementation track because they import the same public mechanisms used by the capstone:

- `../tracks/python-fastapi/tests/`
- `../tracks/typescript-fastify/test-event-core/`

Shared language-neutral cases live under `../shared/vectors/`. Course-level orchestration is implemented by `../../scripts/course_tool.py`. This directory exists to make proof ownership explicit; it is not a third test suite.

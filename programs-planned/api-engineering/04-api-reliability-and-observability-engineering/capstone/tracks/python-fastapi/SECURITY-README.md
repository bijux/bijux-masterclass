# Security Extension

`src/analysis_service/` is the Course 2 durable service. `src/api_security/` is the Course 3 security core and FastAPI adapter. The package separation makes the predecessor visible and avoids pretending that security is a route decorator. See the course-book workshops before integrating controls into production code.

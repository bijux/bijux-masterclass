# Module 05: Resources and Evolution

Correct object models still fail if they leak resources, blur failure handling, or
cannot evolve safely. This module treats survivability as part of design quality.

## Main questions

- Who owns files, sockets, connections, and cleanup obligations?
- How do you group changes and failure boundaries coherently?
- What makes retries safe or unsafe?
- Which modules are public contracts and which are implementation detail?
- How do you add new behavior without quietly breaking old callers?

## Outcome

You should finish this module able to shape object-oriented Python systems that stay
operable and maintainable under long-term change rather than only under greenfield conditions.

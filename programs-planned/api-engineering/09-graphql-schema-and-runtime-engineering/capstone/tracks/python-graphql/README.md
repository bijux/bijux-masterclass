# Python reference track

The Python track is an idiomatic reference for the Course 9 semantics. Its
`graph_api` package contains stable global identifiers, signed high-water
cursors, the bounded operation parser, demand analysis, persisted-operation
admission, request-scoped loaders, service clients, authorization policy,
mutation delegation, partial-data handling, resumable subscriptions, transport
admission, and release decisions.

The dependency-light semantic core uses the Python standard library so that the
mechanisms can be studied and tested without an external registry. It is not
presented as a standards-complete GraphQL executor. The bounded parser accepts
the released course operation shapes; independent framework validation belongs
to the optional proof route.

`src/graph_api/adapters/strawberry_app.py` demonstrates where the same policies
attach to a complete Strawberry runtime. In a provisioned environment:

```bash
python -m pip install -e .
```

Run the semantic track from the course root with `make python-proof`. Learners
using Python as their primary track should also run the loopback laboratory and
trace source call counts for composition, authorization denial, and partial
failure.

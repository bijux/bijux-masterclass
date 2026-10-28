# Python generator evidence

The checked-in handwritten client under `clients/python/src/` is the stable teaching implementation. The generator-owned SDK is disposable and created under `generated/sdk/`.

From `capstone/`, run:

```bash
make clients-generate
```

The route invokes the pinned `openapi-python-client` against `spec/dist/openapi.client.yaml`. Generated code is reviewed through import/build and consumer workflow tests; it is never edited to hide generator limitations. A missing generator is recorded as **not executed**, not as feature support or failure.

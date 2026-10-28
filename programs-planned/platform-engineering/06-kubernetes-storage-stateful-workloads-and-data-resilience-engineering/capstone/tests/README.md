# Capstone tests

Run with:

```bash
PYTHONPATH=capstone python3 -m unittest discover -s capstone/tests -p 'test_*.py' -v
```

The tests prove semantic and local mechanism behavior. They do not replace native Kubernetes, CSI, storage-system, or cloud evidence.

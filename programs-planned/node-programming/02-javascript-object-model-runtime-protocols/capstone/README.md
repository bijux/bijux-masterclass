# ObjectAtlas

ObjectAtlas is the Course 2 cumulative product: a persistent component graph whose runtime object model is explicit and testable.

```text
objectatlas add <id> <folder|component|service> <label> [--parent <id>]
objectatlas set <id> <key> <json-value>
objectatlas delete-attribute <id> <key>
objectatlas move <id> <new-parent|root>
objectatlas remove <id>
objectatlas clone <source-id> <new-root-id>
objectatlas show <id>
objectatlas inspect <id>
objectatlas walk [id] [--order preorder|postorder|breadth]
objectatlas summary
objectatlas help
objectatlas version
```

The storage path defaults to `object-atlas.json` and may be overridden with `OBJECT_ATLAS_FILE`.

The implementation demonstrates:

- complete descriptors and hidden symbol metadata;
- kind policy delegation;
- receiver-safe command routing;
- private branded node state;
- capability-separated application, codec, storage, and rendering layers;
- symbol-keyed conversion, tagging, iteration, and Node inspection;
- lazy deterministic traversal with structural-revision invalidation;
- revocable transactional attribute drafts;
- domain-aware subtree cloning;
- plain versioned persistence;
- deterministic cleanup of edit sessions.

Run:

```bash
npm run typecheck
npm test
npm run demo
```

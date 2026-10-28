# Exercises — OCI images and content addressability

Work these problems before opening the answer file. Each question asks for a decision, failure analysis, or evidence argument—not a recalled definition. Record assumptions and name the strongest claim your evidence can support.
## 1. Why must a descriptor verify media type, digest, and size rather than digest alone?

Write your answer and evidence plan here before comparing it with the worked solution.

## 2. A layer is recompressed with a different gzip timestamp. Predict the blob digest and DiffID changes.

Write your answer and evidence plan here before comparing it with the worked solution.

## 3. Explain why the image configuration digest changes when only `Env` changes.

Write your answer and evidence plan here before comparing it with the worked solution.

## 4. Apply this sequence: Layer A creates `/app/a` and `/app/b`; Layer B adds `/app/.wh.a`; Layer C marks `/app` opaque and adds `/app/c`. What remains?

Write your answer and evidence plan here before comparing it with the worked solution.

## 5. Why can final-rootfs scanning miss a leaked credential?

Write your answer and evidence plan here before comparing it with the worked solution.

## 6. Distinguish an image manifest from an image index.

Write your answer and evidence plan here before comparing it with the worked solution.

## 7. A manifest descriptor says `linux/arm64`, but the executable ELF header is x86-64. Which stage should reject it?

Write your answer and evidence plan here before comparing it with the worked solution.

## 8. List five tar metadata fields that can break reproducible layer digests.

Write your answer and evidence plan here before comparing it with the worked solution.

## 9. Why is `history.created_by` not trustworthy build provenance?

Write your answer and evidence plan here before comparing it with the worked solution.

## 10. An SBOM artifact refers to yesterday’s image digest while today’s tag has moved. Should promotion pass?

Write your answer and evidence plan here before comparing it with the worked solution.

## 11. Explain how a writable container layer differs from an image layer.

Write your answer and evidence plan here before comparing it with the worked solution.

## 12. Design a proof that a reconstructed rootfs matches the manifest and configuration rather than merely “looks correct.”

Write your answer and evidence plan here before comparing it with the worked solution.

## Continue

- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Chapter](index.md)

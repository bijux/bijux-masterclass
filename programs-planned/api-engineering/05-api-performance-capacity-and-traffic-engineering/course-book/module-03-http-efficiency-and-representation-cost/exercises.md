# Module 03 exercises — HTTP Efficiency and Representation Cost

Solve these without opening the answer file. Show assumptions, units, populations, and the decisive oracle. A numerical result without its interpretation is incomplete.

## 1. For a 1,000-byte object, normalize `bytes=100-199`.

Provide a defensible engineering answer and name the evidence needed to verify it.

## 2. Normalize `bytes=-200` for a 1,000-byte object.

Provide a defensible engineering answer and name the evidence needed to verify it.

## 3. What response should `bytes=1500-` receive for a 1,000-byte object?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 4. Why can a content hash be a strong ETag for an artifact?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 5. When is `Cache-Control: no-cache` different from `no-store`?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 6. Why may `Vary: Authorization` be insufficient as a shared-cache security design?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 7. Calculate application buffer for 200 streams, 64 KiB chunks, and two buffers per stream.

Provide a defensible engineering answer and name the evidence needed to verify it.

## 8. A 900-byte JSON response compresses to 600 bytes but costs 1.5 ms CPU. Should it be compressed?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 9. What must remain true when replacing a full download with ranges?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 10. Why measure storage reads for a 304 response?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 11. Can a weak ETag satisfy `If-Range` in this course profile?

Provide a defensible engineering answer and name the evidence needed to verify it.

## 12. Design an experiment for chunk size.

Provide a defensible engineering answer and name the evidence needed to verify it.

## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.

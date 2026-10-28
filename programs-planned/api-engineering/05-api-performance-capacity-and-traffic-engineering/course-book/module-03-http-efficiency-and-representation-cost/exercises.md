# Exercises — Module 03: HTTP Efficiency and Representation Cost

Work through all twelve problems before opening the answers. In **HTTP Efficiency and Representation Cost**, every response must settle this question: **Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?** Do not stop at terminology. Show how the decision changes a request, durable state, consumer, operator action, or release result, and state how that consequence is tested.

## 1. For a 1,000-byte object, normalize `bytes=100-199`.


## 2. Normalize `bytes=-200` for a 1,000-byte object.


## 3. What response should `bytes=1500-` receive for a 1,000-byte object?


## 4. Why can a content hash be a strong ETag for an artifact?


## 5. When is `Cache-Control: no-cache` different from `no-store`?


## 6. Why may `Vary: Authorization` be insufficient as a shared-cache security design?


## 7. Calculate application buffer for 200 streams, 64 KiB chunks, and two buffers per stream.


## 8. A 900-byte JSON response compresses to 600 bytes but costs 1.5 ms CPU. Should it be compressed?


## 9. What must remain true when replacing a full download with ranges?


## 10. Why measure storage reads for a 304 response?


## 11. Can a weak ETag satisfy `If-Range` in this course profile?


## 12. Design an experiment for chunk size.


## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.

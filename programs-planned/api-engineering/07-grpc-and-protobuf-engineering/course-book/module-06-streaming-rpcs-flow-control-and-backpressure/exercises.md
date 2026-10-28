# Exercises — Streaming RPCs, Flow Control, and Backpressure

Answer before opening the reference answers. For every answer, state the governing rule, one failure example, and the evidence that decides the case.

## 1. Choose the RPC shape for GetRun, WatchRun, UploadDataset, and Work.

Write a concise engineering answer and name the decisive proof.

## 2. Why does HTTP/2 flow control not prove bounded application memory?

Write a concise engineering answer and name the decisive proof.

## 3. Define the legal frame order for UploadDataset.

Write a concise engineering answer and name the decisive proof.

## 4. What must happen to a staging file after checksum failure?

Write a concise engineering answer and name the decisive proof.

## 5. Why must a download client verify completion even after receiving many chunks?

Write a concise engineering answer and name the decisive proof.

## 6. Differentiate WatchRun sequence from the public event sequence.

Write a concise engineering answer and name the decisive proof.

## 7. How should a client recover when its WatchRun resume position is outside retention?

Write a concise engineering answer and name the decisive proof.

## 8. Why is an authenticated worker stream insufficient authority to complete an assignment?

Write a concise engineering answer and name the decisive proof.

## 9. What ordering guarantee exists within one gRPC stream, and what can application concurrency break?

Write a concise engineering answer and name the decisive proof.

## 10. Name four independent budgets required for a long-lived stream.

Write a concise engineering answer and name the decisive proof.

## 11. How should a server react to a slow consumer?

Write a concise engineering answer and name the decisive proof.

## 12. Define the proof that backpressure is end-to-end rather than a local queue trick.

Write a concise engineering answer and name the decisive proof.

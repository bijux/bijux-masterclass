# Reference


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  reference["Reference"]
  design["Object design checklist"]
  boundary["Boundary review prompts"]

  reference --> design
  reference --> boundary
```

```mermaid
flowchart LR
  need["Need a stable rule or review aid"] --> choose["Choose the smallest reference page"]
  choose --> design["Design checklist"]
  choose --> boundary["Boundary prompts"]
```
<!-- page-maps:end -->

Use this section when you need stable review standards rather than a reading route.
These pages are meant to stay open while designing or reviewing code, not only while
reading the course front to back.

## Pages in this section

- [Object Design Checklist](object-design-checklist.md) for object-level and aggregate-level design review
- [Boundary Review Prompts](boundary-review-prompts.md) for API, persistence, runtime, and extension pressure

# Standards and profiles

## GraphQL core

The normative baseline is the **GraphQL September 2025 specification**, the latest published release as of 8 August 2026:

- <https://spec.graphql.org/September2025/>

The release includes OneOf Input Objects and the built-in `@oneOf` directive. The course uses that feature in `NodeLookup`.

The latest working draft is not the release baseline. Draft behavior may be discussed as frontier material, but it does not silently enter Analysis Graph API 1.0.

## GraphQL over HTTP

GraphQL core is transport-agnostic. The GraphQL over HTTP specification remains a **Stage 2 draft** as of 8 August 2026:

- <https://graphql.github.io/graphql-over-http/draft/>

The course defines a versioned HTTP profile based on that draft. It supports JSON requests and `application/graphql-response+json`, rejects mutation execution through GET, and distinguishes malformed requests from GraphQL execution errors. Because the source is a draft, the course never labels the profile an official final standard.

## Subscriptions and incremental delivery

The GraphQL core specification defines subscription source and response streams but deliberately does not mandate transport, acknowledgement, replay, or buffering. Course 9 uses a course-specific SSE profile backed by Course 6 events. GraphQL over WebSocket remains optional.

`@defer` and `@stream` are treated as ecosystem frontier features, not as part of the GraphQL September 2025 release. They may be evaluated only through a separately versioned capability matrix.

## Pagination and federation

Cursor connections and global object identification are course profiles influenced by established Relay conventions, not GraphQL core requirements. Apollo Federation examples are optional architecture material, not a claim that federation is the only composition model or a GraphQL Foundation standard.

## Implementation libraries

The optional adapters use Strawberry for Python and GraphQL Yoga/GraphQL.js for TypeScript. Library behavior is subordinate to the released schema and course policies. Tool support is measured rather than assumed.

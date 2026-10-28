/** Released client operation documents used by the dependency-light track. */

export const registeredOperationDocuments: Readonly<
  Record<string, string>
> = {
  CancelAnalysis: `mutation CancelAnalysis(
  $input: CancelAnalysisInput!
) {
  cancelAnalysis(input: $input) {
    ... on CancelAnalysisSuccess {
      clientMutationId
      run { id status version }
    }
    ... on MutationProblem {
      clientMutationId
      code
      message
      field
    }
  }
}
`,

  CreateProject: `mutation CreateProject(
  $input: CreateProjectInput!
) {
  createProject(input: $input) {
    ... on CreateProjectSuccess {
      clientMutationId
      replayed
      project { id name version }
    }
    ... on MutationProblem {
      clientMutationId
      code
      message
      field
    }
  }
}
`,

  GetProjectOverview: `query GetProjectOverview(
  $projectId: ID!
  $first: Int = 20
  $after: Cursor
) {
  project(id: $projectId) {
    id
    name
    version
    analysisRuns(first: $first, after: $after) {
      edges {
        cursor
        node {
          id
          status
          version
          artifacts { id mediaType size sha256 }
          deliverySummary {
            delivered
            pending
            failed
            stalenessSeconds
          }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
`,

  GetRun: `query GetRun($runId: ID!) {
  analysisRun(id: $runId) {
    id
    projectId
    datasetId
    status
    version
    resultSummary
    artifacts {
      id
      mediaType
      size
      sha256
      downloadUrl
    }
    deliverySummary {
      delivered
      pending
      failed
      observedAt
      stalenessSeconds
    }
  }
}
`,

  ListRuns: `query ListRuns(
  $filter: RunFilter
  $first: Int = 20
  $after: Cursor
) {
  analysisRuns(
    filter: $filter
    first: $first
    after: $after
  ) {
    edges {
      cursor
      node { id projectId status version createdAt }
    }
    pageInfo { hasNextPage endCursor }
  }
}
`,

  NodeLookup: `query NodeLookup($by: NodeLookup!) {
  node(by: $by) { __typename id }
}
`,

  RunUpdates: `subscription RunUpdates(
  $runId: ID!
  $afterSequence: String
) {
  analysisRunUpdated(
    runId: $runId
    afterSequence: $afterSequence
  ) {
    sequence
    occurredAt
    run { id status version resultSummary }
  }
}
`,

  SearchPlatform: `query SearchPlatform(
  $text: String!
  $first: Int = 20
  $after: Cursor
) {
  search(text: $text, first: $first, after: $after) {
    edges {
      cursor
      node {
        __typename
        ... on Project { id name }
        ... on AnalysisRun { id status }
        ... on Artifact { id mediaType size }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
`,

  StartAnalysis: `mutation StartAnalysis(
  $input: StartAnalysisInput!
) {
  startAnalysis(input: $input) {
    ... on StartAnalysisSuccess {
      clientMutationId
      replayed
      run { id status version }
    }
    ... on MutationProblem {
      clientMutationId
      code
      message
      field
    }
  }
}
`,

  Viewer: `query Viewer {
  viewer { subject tenantId permissions }
}
`,
};

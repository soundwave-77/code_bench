GET_ISSUES_FROM_PULL_QUERY: str = """
query($repoOwner: String!, $repoName: String!, $pullNumber: Int!) {
  repository(owner: $repoOwner, name: $repoName) {
    pullRequest(number: $pullNumber) {
      closingIssuesReferences(first: 100) {
        nodes {
          title
          url
          number
        }
      }
    }
  }
}
"""

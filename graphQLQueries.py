# Queries
# Commit date - on commit
# Name, isFork, resourcePath, stars, get files in path - on repository

query_ansible_helm = """
query ($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    commitDetails: object(expression: "master") {
      ... on Commit {
        committedDate
      }
    }
    ... on Repository {
      name
      isFork
      resourcePath
      stargazers {
        totalCount
      }
      files: object(expression: "master:build/Dockerfile") {
        ... on Blob {
          text
        }
      }
    }
  }
}"""


query_go = """
query ($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    commitDetails: object(expression: "master") {
      ... on Commit {
        committedDate
      }
    }
    ... on Repository {
      name
      isFork
      resourcePath
      stargazers {
        totalCount
      }
      files: object(expression: "master:go.mod") {
        ... on Blob {
          text
        }
      }
      main: object(expression: "master:cmd/manager/main.go") {
        ... on Blob {
          text
        }
      }
    }
  }
}"""

variable = {
  "owner": "onap",
  "name": "demo"
}

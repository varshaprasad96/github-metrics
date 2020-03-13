
# GraphQL queries which is to be executed
# queryRepo - for initial querying, to get the result of first page
# traverseRepo - to traverse the page, using the endCursor

queryRepo = """
    query topRepos($queryWord: String!) {
      search(first:100, query: $queryWord, type: REPOSITORY) {
        repositoryCount
        nodes {
          ... on Repository {
            name
            resourcePath
          }
        }
        pageInfo {
            hasNextPage
            endCursor
            }
       }
     }
    """

traverseRepo = """
    query topRepos($queryWord: String!, $after: String) {
      search(first:100, after: $after, query: $queryWord, type: REPOSITORY) {
        repositoryCount
        nodes {
          ... on Repository {
            name
            resourcePath
          }
        }
        pageInfo {
            hasNextPage
            endCursor
            }
       }
     }
    """

variables = {
    'queryWord': 'operator-SDK'
}

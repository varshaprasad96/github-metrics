# Implement GraphQL query to fetch the data from github
from queries import queryRepo, traverseRepo, variables
import requests
import logging

# Fill <token> with your respective git-token. Steps to generate token:
# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
HEADERS = {"Authorization": "Bearer <git-token>"}
SDK_REPO = {}


# ExecuteQuery class, consumes the GraphQL queries provided in queries.py and makes a POST request
# to githubAPI to get the response. It further handles pagination, to obtain the response in the
# required format by filling up the dictionary - SDK_REPO.
class ExecuteQuery:

    # run_query executes the GraphAPI call with required parameters.
    def run_query(self, query, var):
        request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': var},
                                headers=HEADERS)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    # Execute to query to obtain the result
    def queryResponse(self, queryToExecute):
        result = ExecuteQuery().run_query(queryToExecute, variables)
        return result

    # Handle pagination and iterate through the list of repositories
    # to get the details.
    def totalListOfRepositories(self):
        resp = ExecuteQuery().queryResponse(queryRepo)
        logging.info("Fetching details after executing the query")
        ExecuteQuery().fillRepo(resp)

        # GitHub restricts the response to 100 objects. Traverse through
        # the pages to get all the repositories.
        while ExecuteQuery().hasNext(resp):

            logging.info("Response has multiple pages, modifying the variables")
            # modify / include the variables to have the $after - endCursor
            ExecuteQuery().modifyQueryVariable(resp['data']['search']['pageInfo']['endCursor'])

            # execute and overwrite the response
            resp = ExecuteQuery().queryResponse(traverseRepo)

            # Fill the list
            ExecuteQuery().fillRepo(resp)

        return ExecuteQuery().returnVariable()

    # Check whether the next page exists.
    def hasNext(self, resp):
        hasNextPage = resp['data']['search']['pageInfo']['hasNextPage']
        return hasNextPage

    # Iterate over the json response, and fill the dictonary with the list
    # of queries.
    def fillRepo(self, response):
        for repo in response['data']['search']['nodes']:
            SDK_REPO[repo['resourcePath']] = repo['name']
        return

    # Modify query variable
    def modifyQueryVariable(self, endCursor):
        logging.info("End cursor which is being added to variables for querying {cursor}".format(cursor=endCursor))
        variables['after'] = endCursor


    def returnVariable(self):
        return SDK_REPO


# Return the entire list of repositories.
def listOfRepositories():
    repositories = ExecuteQuery().totalListOfRepositories()
    print(repositories)
    return repositories

import requests
from urllib.error import HTTPError
import logging
import time


# Query strings. Search for these in all codes of github
ANSIBLE_QUERY = "quay.io/operator-framework/ansible-operator"
GO_QUERY = "github.com/operator-framework/operator-sdk"
HELM_QUERY = "quay.io/operator-framework/helm-operator"

# Files to search
ANSIBLE_HELM_FILENAME = "Dockerfile"
GO_FILENAME = "go.mod"
HEADER = "XXXXXXXXXXXXXXXXXXXX"

class RestApi:

    def __init__(self):
        self.repo = set()

    # Handle pagination. Traverse through the response items, store repository name in a set.
    def getlist(self, query_parameter, pages, filename):
        for pg in range(1, pages+1):
            req_string = "https://api.github.com/search/code?q="+query_parameter+\
                         "in:"+filename+"&access_token=" + HEADER + "&page=" + \
                         str(pg) + "&per_page=100"
            try:
                response = requests.get(req_string)
                for repo in response.json()['items']:
                    self.repo.add(repo['repository']['full_name'])
            except HTTPError:
                logging.info(HTTPError)
            time.sleep(5)

    def returnlist(self, query_parameter, pages, filename):
        self.getlist(query_parameter, pages, filename)
        return self.repo

# TODO: No of pages are hardcoded. Try finding (total number/100) pass it.
def get_go_repositories():
    go_repo = RestApi().returnlist(query_parameter=GO_QUERY, pages=6, filename=GO_FILENAME)
    return go_repo


def get_ansible_repositories():
    ansible_repo = RestApi().returnlist(query_parameter=ANSIBLE_QUERY, pages=2, filename=ANSIBLE_HELM_FILENAME)
    return ansible_repo


def get_helm_repositories():
    helm_repo = RestApi().returnlist(query_parameter=HELM_QUERY, pages=2, filename=ANSIBLE_HELM_FILENAME)
    return helm_repo

# To test rest_api
"""
def main():
    repo_list = RestApi().returnlist(query_parameter=ANSIBLE_QUERY, pages=1, filename=ANSIBLE_HELM_FILENAME)
    print(repo_list)

if __name__ == '__main__':
    main()
"""
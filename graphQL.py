# Based on the repo_list obtained from rest_api, send graph_QL queries to fetch
# required data

import re
import requests
from graphQLQueries import query_ansible_helm, query_go, variable

HEADERS = {"Authorization": "Bearer #################"}

class GraphQLQuery:

    def __init__(self, list_of_repo):
        self.repo_to_query = list_of_repo   # Output repo from rest_api
        self.repoVersion = {}               # Dict (repo_name: version)
        self.go_operators_count = 0         # Get go_operator_count - some of them dont have main.go
        self.version_details = {}           # (repo_name: version)
        self.repo_stargazers = {}           # (repo_name: stars)

    def run_query(self,query, var):
        request = requests.post('https://api.github.com/graphql',
                                json={'query': query, 'variables': var}, headers=HEADERS)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}.".format(request.status_code))

    # Pass the kind of operator, so that the required query can be executed
    def repo_versions(self, operator):
        print("Executing")

        # Repo list has operator_owner/repo_name format
        for repo in self.repo_to_query:
            details = repo.split("/")
            owner = details[0]
            name = details[1]

            variable['owner'] = owner
            variable['name'] = name

            if operator == "go":
                response = self.run_query(query_go, variable)
            else:
                response = self.run_query(query_ansible_helm, variable)

            # Get version if present
            if response.get('data')['repository']['files'] is not None:
                self.repoVersion[name] = self.get_version(response.get('data')['repository']['files']['text'])

            # For go-operator. Check cmd/manager/main.go
            if ('main' in response.get('data')['repository']) and \
                    (response.get('data')['repository']['main']) is not None:
                self.go_operators_count = self.go_operators_count + 1

            # Get the star-gazers count
            if response.get('data')['repository']['stargazers']['totalCount'] != 0:
                self.repo_stargazers[name] = response.get('data')['repository']['stargazers']['totalCount']

        return self.repoVersion

    def get_version(self, text):

        go_regex = re.compile("operator-sdk\s+v[0-9].[0-9]*.[0-9]*")
        ansible_regex = re.compile("operator-framework/ansible-operator:[a-z]*[0-9]*.[0-9]*.[0-9]*")
        helm_regex = re.compile("operator-framework/helm-operator:[a-z]*[0-9]*.[0-9]*.[0-9]*")

        go_sdk_ver = re.search(go_regex, text)
        ansible_sdk_ver = re.search(ansible_regex, text)
        helm_sdk_ver = re.search(helm_regex, text)

        if go_sdk_ver is not None:
            return go_sdk_ver.group()

        elif ansible_sdk_ver is not None:
            return ansible_sdk_ver.group()

        elif helm_sdk_ver is not None:
            return helm_sdk_ver.group()

    def number_of_go_operators(self):
        return self.go_operators_count

    def version_count(self):
        for name, version in self.repoVersion.items():
            if version in self.version_details:
                count = self.version_details.get(version)
                self.version_details[version] = count + 1
            else:
                self.version_details[version] = 1
        return self.version_details

    def get_stargazers(self):
        return self.repo_stargazers

# Test GraphQL
"""
def main():
    test_list = ['jaredhocutt/gogs-operator',
                 'mcserverhosting-net/mc-operator', 'mittwald/brudi-operator', 'Jooho/jhouse_openshift']

    r = GraphQLQuery(test_list).repo_versions("go")

    print(r)

if __name__ == '__main__':
    main()
"""

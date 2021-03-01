# Run sdk_metrics.py to start up the prometheus server

import rest_api
from graphQL import GraphQLQuery
import logging
from prometheus_client import start_http_server, Gauge

REPOSITORY_COUNT = Gauge('number_of_repositories', 'name_of_the_operator', ['Kind_of_operator'])
ANSIBLE_VERSION_DATA = Gauge('name_of_repositories', 'version_of_operator', ['name', 'version'])
ANSIBLE_VERSION = Gauge('ansible_version', 'version_of_operator', ['version'])
HELM_VERSION = Gauge('helm_version', 'version_of_operator', ['version'])
GO_VERSION = Gauge('go_version', 'version_of_operator', ['version'])
ANSIBLE_STARS = Gauge('ans_repo_stars', 'stars', ['name_of_repository'])
HELM_STARS = Gauge('helm_repo_stars', 'stars', ['name_of_repository'])


if __name__ == '__main__':

    # Get repository names using rest_api. Pass on the list to
    # GraphQL and get required details

    ansible_repo = rest_api.get_ansible_repositories()
    ansible = GraphQLQuery(ansible_repo)
    ansible_version = ansible.repo_versions("ansible")
    ansible_version_stat = ansible.version_count()
    ansible_repo_stars = ansible.get_stargazers()

    # Uncomment only for debug - (or else will slow down the process!)
    # print(len(ansible_version))
    # print(ansible_repo_stars)


    helm_repo = rest_api.get_helm_repositories()
    # print(helm_repo)
    helm = GraphQLQuery(helm_repo)
    helm_version = helm.repo_versions("helm")
    helm_version_stat = helm.version_count()
    helm_repo_stars = helm.get_stargazers()

    # Uncomment only for debug
    # print(helm_version_stat)
    # print(helm_repo_stars)

    go_repo = rest_api.get_go_repositories()
    go = GraphQLQuery(go_repo)
    # go_version = go.repo_versions("go")
    number_of_go_repositories = go.number_of_go_operators()
    go_version_stat = go.version_count()

    # Uncomment only for debug
    # print("number of go operators")
    # print(number_of_go_repositories)
    # print("go_version_stat")
    # print(go_version_stat)

    ################ PROMETHEUS #######################################

    # Start up the server to expose the metrics.
    start_http_server(8000)
    logging.info("Starting Prometheus server")


    while True:
        REPOSITORY_COUNT.labels("Ansible").set(len(ansible_version))
        REPOSITORY_COUNT.labels("Helm").set(len(helm_version))
        REPOSITORY_COUNT.labels("Go").set(number_of_go_repositories)

        for name, version in ansible_version.items():
            ANSIBLE_VERSION_DATA.labels(name, version).set(1)

        # Iterate to get ansible versions:
        for version, count in ansible_version_stat.items():
            if version is not None:
                details = version.split(":")
                ver = details[1]
                ANSIBLE_VERSION.labels(ver).set(count)

        # Iterate to get helm version:
        for version, count in helm_version_stat.items():
            if version is not None:
                details = version.split(":")
                ver = details[1]
                HELM_VERSION.labels(ver).set(count)

        # Iterate to get go version:
        for version, count in go_version_stat.items():
            if version is not None:
                details = version.split(" ")
                ver = details[1]
                GO_VERSION.labels(ver).set(count)

        # Iterate to log ansible stargazers:
        for name, stars in ansible_repo_stars.items():
            # Do not include operator-sdk itself
            if name != "operator-sdk":
                ANSIBLE_STARS.labels(name).set(stars)

        # Iterate to log helm stargazers:
        for name, stars in helm_repo_stars.items():
            if name != "operator-sdk":
                HELM_STARS.labels(name).set(stars)

from prometheus_client import start_http_server, Gauge
import time
from getData import listOfRepositories
import logging

# Create a metric to track the number of repositories and their details
REPOSITORY_COUNT = Gauge('number_of_repositories', 'repository_count')
REPOSITORY_DETAILS = Gauge('resource_path_of_repository', 'list_of_repositories', ['name', 'path'])

# Enable logging
logging.basicConfig(level=logging.INFO)

# Run the prometheus server. After an interval of every 100 seconds
# query GitHub to get the list of repositories which use Operator-SDK
# and expose it at the endpoint.

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    logging.info("Starting Prometheus server")

    # Get the list of SDK repositories
    sdkRepositories = listOfRepositories()
    logging.info("Number of repositories is {len}".format(len=len(sdkRepositories)))

    # Update the repository count and the details regularly
    # after every 100 seconds.
    while True:
        REPOSITORY_COUNT.set(len(sdkRepositories))

        for name, path in sdkRepositories.items():
            REPOSITORY_DETAILS.labels(name, path).set(1)

        time.sleep(100)
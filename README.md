# github-metrics
Utilize GraphQL API to get the reachability metrics about Operator-SDK

The project utilizes GraphQL to scrape GitHub and obtain data about Operator-SDK.

Things-done:
 - Scrape github to get the list of repositories which use Operator-SDK.
 - Traverse through multiple pages to get the data.
 - Expose to prometheus.
 - Create Grafana dashboard.

Things TO-DO:
- Remove forks / cloned repositories.
- Collect additional metrics (version etc)

## Running Script

Run:  
```bash
$ python prom-expose.py
```
Metrics exposed on http://localhost:8000

Output:

1. Data exposed at endpoint for Prometheus to scrape it:
![Image of Yaktocat]:

2. Data exposed in prometheus:
![Image]

3. Same graph (just one metric is used as of now)
[!Image]
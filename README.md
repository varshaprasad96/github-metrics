# github-metrics
Utilize GraphQL API and RestAPI to get the reachability metrics about Operator-SDK

The project utilizes GraphQL to scrape GitHub and obtain data about Operator-SDK.

Things-done:
 - Scrape github to get the list of repositories which use Operator-SDK - RestAPI.
 - Traverse through multiple pages to get the data.
 - Check for patterns in repositories.
 - Use GraphQL to update data.
 - Expose to prometheus.
 - Create Grafana dashboard.

Things TO-DO:
- Work on gopkg.toml files
- Collect additional metrics (version etc)
- Process commit history

## Running Script

Run:  
```bash
$ python sdk-metrics.py
```
Metrics exposed on http://localhost:8000

Output:

1. Data exposed at endpoint for Prometheus to scrape it:
![Image](https://github.com/varshaprasad96/github-metrics/blob/dev/output_images/Data-at-endpoint.png)

2. Data exposed in prometheus:
![Image-Data](https://github.com/varshaprasad96/github-metrics/blob/dev/output_images/Prometheus-data.png)

3. Same graph (just one metric is used as of now) -  Similar graph is also obtained in grafana
![Image-graph](https://github.com/varshaprasad96/github-metrics/blob/dev/output_images/Example-Graph.png)

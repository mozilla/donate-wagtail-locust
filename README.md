donate-wagtail-locust
---------------------

This project aims to help us in capacity planning for the new wagtail based donation platform we're launching in late 2019.

### Running with Docker locally

1. `docker build -t donate-locust .`
2. Copy the sample environment file, and customize it to your needs: `cp sample.env .env`.
3. `docker run --env-file .env -p 8089:8089 --add-host "localhost:$HOST_IP_ADDR" -it donate-locust`
 
#### Environment variables

| Variable           |                                                                             Description                                                                            |
|--------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| TARGET_URL         |  The hostname (including protocol) of the wagtail-donate stack to test. Required.                                                                                  |
| LOCUST_MODE        | Start locust in the specified mode. One of `standalone`, `leader`, or `follower`. Optional, defaults to `standalone`                                               |
| LOCUST_LEADER_HOST |  When running in distributed mode, this variable tells followers where to connect to the leader node. Required when `LOCUST_MODE` is `standalone`                  |
| LOCUST_LEADER_PORT |  When running in distributed mode, this variable tells followers what port number the leader mode is listening for follower nodes on. optional, defaults to `5557` |

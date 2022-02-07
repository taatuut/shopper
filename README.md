# Shopper

## Prerequisites

* A local MongoDB installation, version 4.4 or higher
* A MongoDB Atlas account, you can use free tier cluster
* MongoDB Compass
* `mongoimport` database tool
* This repo

## Connection strings

### Local
`mongodb://localhost:27017/shopper`

### Atlas
Get the connection string from the Atlas interface for the cluster you want to use, you need to change *user name* and *password*, use *shopper* as *database name*. 

`mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper` <- 

# Local

0. Start MongoDB locally

```
cd path/to/shopper
mkdir -p /tmp/data/db
mongod --dbpath /tmp/data/db
```

1. Run `python3 create_order.py` as a test

2. Run `python3 create_order.py | mongoimport --uri "mongodb://localhost:27017/shopper" --collection order --jsonArray`

3. Start Compass: connect, analyze schema, select, create index, export code, aggregation framework.

4. Uncomment local connection string in `query_order.py` and run `python3 query_order.py`. Note that the query uses a random point so number of results can vary (0 or more).

# Atlas

5. Run `python3 create_order.py | mongoimport --uri "mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper" --collection order --jsonArray`

6. Check Compass tasks (see above).

7. Uncomment Atlas connection string in `query_order.py` and run `python3 query_order.py`

## Repetitive load and query to Atlas

8. To load data continuously run the following command in a terminal

`cd path/to/shopper`

_local_

`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri mongodb://localhost:27017/shopper --collection order --jsonArray; sleep 5; done`

_Atlas_

`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper --collection order --jsonArray; sleep 5; done`

9. To query continuously, run the below command after setting the right connection string for _local_ or _Atlas_ in `query_order.py`

`clear; while :; do echo $(date); python3 query_order.py; sleep 5; done`

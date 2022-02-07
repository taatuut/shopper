# Shopper

The Shopper repo demoes ingesting online groceries orders, and querying with a spatial query.

Shopper uses multiple tools to work with the order data: the `mongoimport` database tool for 'batch loading' and `Pymongo` driver to run a specific query in a Python script.

## Prerequisites

* MongoDB installed local, version 4.4 or higher https://docs.mongodb.com/manual/installation/ and/or
* A MongoDB Atlas account, you can use the free tier cluster https://docs.atlas.mongodb.com/getting-started/
* MongoDB Compass, a user friendly desktop tool for data exploration and management https://www.mongodb.com/products/compass
* A recent Python 3 installation, version 3.6 or higher with the `Pymongo` driver https://docs.mongodb.com/drivers/pymongo/ something like `python3 -m pip install pymongo`
* The `mongoimport` database tool https://www.mongodb.com/try/download/database-tools
* This repo :-) https://github.com/taatuut/shopper

## Connection strings

Use *shopper* as default *database name*.

### Local
`mongodb://localhost:27017/shopper`

### Atlas
Get the connection string from the Atlas interface for the cluster you want to use, you need to change *user name*, *password* and *database name*. 

`mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper`

# Local

0. Start MongoDB locally using somethig like:

```
cd path/to/repo/folder/shopper
mkdir -p /tmp/data/db
mkdir -p /tmp/data/log
mongod --fork --logpath /tmp/data/log/mongod.log --dbpath /tmp/data/db
```

1. Run `python3 create_order.py` as a test, this will write set of orders to the console

2. Run `python3 create_order.py | mongoimport --uri "mongodb://localhost:27017/shopper" --collection order --jsonArray`

3. Start Compass: connect, analyze schema, change daat model on the fly, select, create spatial index, export code, aggregation framework.

4. Uncomment _local_ connection string in `query_order.py` and run `python3 query_order.py`. Note that the query uses a random point so number of results can vary (0 or more).

# Atlas

5. Run `python3 create_order.py | mongoimport --uri "mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper" --collection order --jsonArray`

6. Check Compass tasks (see step 3. above).

7. Uncomment _Atlas_ connection string in `query_order.py` and run `python3 query_order.py`

## Repetitive load and query to Atlas

8. To load data continuously run the following command in a terminal

`cd path/to/repo/folder/shopper`

_local_

`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri mongodb://localhost:27017/shopper --collection order --jsonArray; sleep 5; done`

_Atlas_

`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper --collection order --jsonArray; sleep 5; done`

9. To query continuously, run the below command after setting the right connection string for _local_ or _Atlas_ in `query_order.py`

`clear; while :; do echo $(date); python3 query_order.py; sleep 5; done`

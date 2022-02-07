# Shopper

## Prerequisites

* MongoDB local
* MongoDB Atlas
* mongoimport
* This repo

## Connection strings

### Local
mongodb://localhost:27017/shopper

### Atlas

mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper

# Local

0. Start MongoDB locally

cd ~/Github/taatuut/shopper
mkdir -p /tmp/data/db
mongod --dbpath /tmp/data/db

1. Run `python3 create_order.py` as a test

2. Run `python3 create_order.py | mongoimport --uri "mongodb://localhost:27017/shopper" --collection order --jsonArray`

3. Start Compass: connect, analyze schema, select, export code

4. Uncomment local connection string in `query_order.py` and run `python3 query_order.py`

# Atlas

5. Run `python3 create_order.py | mongoimport --uri mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper --collection order --jsonArray`

6. In Compass: connect, analyze schema, select, export code

7. Uncomment Atlas connection string in `query_order.py` and run `python3 query_order.py`

## Repetitive load and query to Atlas

8. To load data continuously run the following command in a terminal

`cd ~/Github/taatuut/shopper`

_local_
`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri mongodb://localhost:27017/shopper --collection order --jsonArray; sleep 5; done`

_Atlas_
`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper --collection order --jsonArray; sleep 5; done`

9. To query continuously run below command after setting the right connection string in `query_order.py`

`clear; while :; do echo $(date); python3 query_order.py; sleep 5; done`

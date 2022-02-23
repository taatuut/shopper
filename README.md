# Shopper

The Shopper repo demoes ingesting online groceries orders, and querying with a spatial query.

 ![Example: 'digitale kassabon' in the AH app](images/800_digitalekassabonindeahapp.jpg)

Shopper uses multiple tools to work with the order data: the `mongoimport` database tool for 'batch loading' and `Pymongo` driver to run a specific query in a Python script.

Code was written on MacOS, mainly Python with a bit of bash code. Some alternative command prompt code for Windows is mentioned in this readme.

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
Get the connection string from the Atlas user interface for the cluster you want to use, you need to change *user name*, *password* and *database name*.

`mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper`

Set atlas_uri as an environment variable to avoid storing connection strings, passwords and the alike in code

On MacOS, Linux

`export atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/shopper`

For a local MongoDB installation use `export atlas_uri=mongodb://localhost:27017/shopper`

On Windows

For Atlas `set atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/shopper`

Retrieve with `$atlas_uri` or `%atlas_uri` on MacOS or Windows, and `atlas_uri = os.getenv('atlas_uri')` in Python.

# Prepare

## Start local MongoDB using somethig like:

```
cd path/to/repo/folder/shopper
mkdir -p /tmp/data/db
mkdir -p /tmp/data/log
mongod --fork --logpath /tmp/data/log/mongod.log --dbpath /tmp/data/db
```

## Get familiar with the data

Examine the file [order.json](order.json) to get an idea of the digital order data model.

# Local

1. Run `python3 create_order.py` as a test, this writes a set of orders to the console, using the digital order data model in `order.json`.

2. Run `python3 create_order.py | mongoimport --uri "mongodb://localhost:27017/shopper" --collection order --jsonArray` to pipe the order stream through `mongoimport` to your local MongoDB installation. Note that the `shopper` database and `order` collection are automatically create if not there. 

3. Start Compass: connect to the database, change data model on the fly, analyze the schema, query using tehn map, create a spatial index, export code, add to aggregation framework, create a view. See the video at <TODO>.

4. Uncomment _local_ connection string in `query_order.py` and run `python3 query_order.py`. Note that the query uses a random point so number of results will vary (0 or more).

# Atlas

5. Run `python3 create_order.py | mongoimport --uri "mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper" --collection order --jsonArray` or with environment variable `python3 create_order.py | mongoimport --uri "$atlas_uri" --collection order --jsonArray`

6. Check Compass tasks (see step 3. above).

7. Uncomment _Atlas_ connection string in `query_order.py` and run `python3 query_order.py`

## Repetitive load and query to Atlas

8. To ingest orders continuously set the right `atlas_uri` and run the following command in a terminal from the `shopper` folder:

`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri $atlas_uri --collection order --jsonArray; sleep 5; done`

9. To query continuously, run the below command after setting the right connection string for _local_ or _Atlas_ in `query_order.py`

`clear; while :; do clear; echo $(date); python3 query_order.py; sleep 5; done`

# Charts

 ![Example: Product sales](images/charts.png)

# Online archive

<TODO> 

 ![Example: Automatically offload 'old' digital receipts](images/OnlineArchive.png)

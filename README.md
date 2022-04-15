# Shopper

The Shopper application demoes ingesting online groceries orders, and querying with a geospatial query.

 ![Example: 'digitale kassabon' in the AH app](images/800_digitalekassabonindeahapp.jpg)

Shopper uses multiple tools to work with the order data: the `mongoimport` database tool for 'batch loading' and `Pymongo` driver to run a geospatial query in a Python script. In addition there is a small Maven Java project that provides similar query functionality using the MongoDB synchronous Java driver.

The code is written on MacOS usign `VS Code`, mainly Python and Java with a bit of javascript and bash code. Some alternative command prompt code for Windows is mentioned in this readme.

## Prerequisites

* This repo :nerd_face: https://github.com/taatuut/shopper
* MongoDB synchronous Java driver https://github.com/mongodb/mongo-java-driver add dependency to `pom.xml`

* Preferably an MongoDB Atlas account, cause we will use Search and Data Lake (work in preparation...). You can use the free tier cluster https://docs.atlas.mongodb.com/getting-started/

I'm using Homebrew on my Mac to easily install and manage most of the following components https://brew.sh/
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Homebrew requires the Xcode command-line tools from Apple's Xcode
`xcode-select --install`

* MongoDB installed local, version 4.4 or higher https://docs.mongodb.com/manual/installation/
`brew tap mongodb/brew` then `brew install mongodb-community@5.0`
* MongoDB Compass, a user friendly desktop tool for data exploration and management https://www.mongodb.com/products/compass
`brew install --cask mongodb-compass`

* A recent Python 3 installation, version 3.6 or higher
`brew install python` or for a specific version `brew install python@3.10`
* The `Pymongo` driver https://docs.mongodb.com/drivers/pymongo/
`python3 -m pip install pymongo` where 'python3' should match the path to your Python executable
* The `mongoimport` database tool https://www.mongodb.com/try/download/database-tools Starting with MongoDB 4.4.1, installing the MongoDB Server via Homebrew also installs the Database Tools. The following command will determine if the Database Tools are already installed on your system:
`brew list | grep mongodb-database-tools`
If not there do `brew install mongodb-database-tools` and to upgrade run `brew upgrade mongodb-database-tools`
* Java
`brew install openjdk`
* Maven
`brew install maven`

And using Nodejs, NPM to install some other tools.

* nodejs, npm
`brew install node`
* mgeneratejs https://github.com/rueckstiess/mgeneratejs
`npm install -g mgeneratejs`

## Connection strings
Use *shopper* as default *database name*.

### Local
`mongodb://localhost:27017/shopper`

### Atlas
Get the connection string from the Atlas user interface for the cluster you want to use, you need to set *user name*, *password* and *database name*.

`mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper`

Set atlas_uri as an environment variable to be able to retrieve it from both Python script and Java jar (and to avoid storing connection strings, passwords and the alike in code...).

On MacOS, Linux

`export atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/shopper`

For a local MongoDB installation use `export atlas_uri=mongodb://localhost:27017/shopper`

On Windows

For Atlas `set atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/shopper`

Retrieve with `$atlas_uri` or `%atlas_uri` in a terminal on MacOS or Windows, `atlas_uri = os.getenv('atlas_uri')` in Python, and `System.getenv("atlas_uri");` in Java.

# Prepare
When usign a local MongoDB installation, start it using something like:

```
cd path/to/repo/folder/shopper
mkdir -p /tmp/data/db
mkdir -p /tmp/data/log
mongod --fork --logpath /tmp/data/log/mongod.log --dbpath /tmp/data/db
```

## Get familiar with the data
Examine the file [order.json](order.json) with a made up concept of the digital order data model.

Based on the file `order.json` there is also template file [order_template.json](order_template.json) to use with `mgeneratejs`.

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

![Example: Automatically offload 'old' digital receipts](images/OnlineArchive.png)

# Search

# Data Lake

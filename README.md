# Shopper

The Shopper application demoes ingesting online groceries orders, and querying with a geospatial query.

 ![Example: 'digitale kassabon' in the AH app](images/800_digitalekassabonindeahapp.jpg)

Shopper uses multiple tools to work with the order data: the `mongoimport` database tool for 'batch loading' and `Pymongo` driver to run a geospatial query in a Python script. In addition there is a small Maven Java project that provides similar query functionality using the MongoDB synchronous Java driver.

The code is written on MacOS using `VS Code`, mainly in Python and Java with a bit of javascript and few lines of code to run in the terminal. Some alternative command prompt code for Windows is mentioned in this readme.

## Prerequisites

I'm using Homebrew on my Mac to easily install and manage most of the following components (NOTE: I'm presales so my development environment standards might tend towards q&d a bit) https://brew.sh/

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Homebrew requires the Xcode command-line tools from Apple's Xcode

`xcode-select --install`

* This repo :nerd_face: https://github.com/taatuut/shopper

* Preferably an MongoDB Atlas account, cause we will use Search and Data Lake (work in preparation...). You can use the free tier cluster https://docs.atlas.mongodb.com/getting-started/

Of course you can also run this with MongoDB installed locally (use version 4.4 or higher https://docs.mongodb.com/manual/installation/)

`brew tap mongodb/brew` then `brew install mongodb-community@5.0`

* MongoDB Compass, a user friendly desktop tool for data exploration and management https://www.mongodb.com/products/compass

`brew install --cask mongodb-compass`

* A recent Python 3 installation, version 3.6 or higher

`brew install python` or for a specific version `brew install python@3.10`

* The `Pymongo` driver https://docs.mongodb.com/drivers/pymongo/

`python3 -m pip install pymongo` where 'python3' should match the path to your Python executable

* Maven

`brew install maven`

* Java

`brew install openjdk`

* MongoDB synchronous Java driver https://github.com/mongodb/mongo-java-driver the dependency is already added to `pom.xml`

* The `mongoimport` database tool https://www.mongodb.com/try/download/database-tools Starting with MongoDB 4.4.1, installing the MongoDB Server via Homebrew also installs the Database Tools. The following command will determine if the Database Tools are already installed on your system:

`brew list | grep mongodb-database-tools`
If not there do `brew install mongodb-database-tools` and to upgrade run `brew upgrade mongodb-database-tools`

* And using Nodejs, NPM to install some other tools like `mgeneratejs`.

`brew install node`

* mgeneratejs https://github.com/rueckstiess/mgeneratejs

mgeneratejs generates structured, semi-random JSON data according to a template object. It offers both a command line script and a JavaScript API. We will use it to create order data in addition to a Python script with a similar purpose.

`npm install -g mgeneratejs`

## Connection string

Use *shopper* as default *database name*.

Get the connection string from the Atlas user interface for the cluster you want to use, you need to set *user name*, *password* and *database name*.

`mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/shopper`

With a standard local installation you can use `mongodb://localhost:27017/shopper`

Set atlas_uri as an environment variable to be able to retrieve it from both Python script and Java jar (and to avoid storing connection strings, passwords and the alike in code...).

*On MacOS, Linux*

`export atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/shopper`

With a local MongoDB installation use `export atlas_uri=mongodb://localhost:27017/shopper`

*On Windows*

For Atlas `set atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/shopper`

Retrieve with `$atlas_uri` or `%atlas_uri` in a terminal on MacOS or Windows, in Python use `atlas_uri = os.getenv('atlas_uri')`, and `System.getenv("atlas_uri");` in Java.

# Prepare

When you have created an Atlas cluster you are ready to go. With MongoDB local, kick it off using something like:

```
mkdir -p /tmp/data/db
mkdir -p /tmp/data/log
mongod --fork --logpath /tmp/data/log/mongod.log --dbpath /tmp/data/db
```

## Get familiar with the data

Examine the file [order.json](order.json) with a made up concept of the digital order data model. Of course you can adapt this as you wish because the flexible document model allow you to change the structure. At the moment it use a geojson like structure, with `geometry` for the coordinates, and `properties` for the attribute fields.

Based on the file `order.json` there is also template file [order_template.json](order_template.json) to use with `mgeneratejs`.

# Test

Set `atlas_uri` if not done before.

1. Run `python3 create_order.py` as a test, this writes a set of orders to the console, with a similar digital order data model as in `order.json`. This script also adds some random notes in Dutch to the order. This information is useful to query with full text search provided by Atlas Search. Besides that there is also the order template json file that mgeneratejs uses to create data. This does not include the option to add notes in Dutch.

2. Run `python3 create_order.py | mongoimport --uri $atlas_uri --collection orders --jsonArray` to pipe the orders output of the Python script directly through `mongoimport` to your MongoDB database. Note that the `shopper` database and `orders` collection are automatically created if they do not exist. 

3. Start Compass: connect to the database, change data model on the fly, analyze the schema, query using the map, create a spatial index to speed up querying, export code in your preferred programming language, create a search index on the notes, add full text search to an aggregation framework data pipeline, create a view with aggregated results on revenue per product. <!--TODO: See the video at xxx.-->

4. Run `python3 query_order.py`. Note that the query uses a random point in a rectangle roughly covering the Netherlands. The number of results will vary (0 or more). In the next step we will also use the Java project to continuously query the database.

## Repetitive load and query

1. To ingest a certain amount of orders, run the following command in a terminal from the `shopper` folder:

`mgeneratejs order_template.json -n 1000 | mongoimport --uri $atlas_uri --collection orders`

Or to run continuously, use the  Python script `create_order.py` from Test step 1:

`clear; while :; do echo $(date); python3 create_order.py | mongoimport --uri $atlas_uri --collection orders --jsonArray; sleep 5; done`

2. Create the jar for the Java project (it is included in the repo, but might be good to create your own to match library and driver versions).

Run `java -jar shopper.jar` to list the required input options:

```
Missing required options: n, r
usage: Shopper Info
 -n,--requests <arg>   Number of requests
 -r,--interval <arg>   Request interval (seconds)
 ```

Now run like `java -jar shopper.jar -n 3 -r 5` to send three queries with a random location every five seconds.

As an alternative to the Java app, run the following command:

`clear; while :; do clear; echo $(date); python3 query_order.py; sleep 5; done`

# Charts

MongoDB Atlas Charts enables you to visualize real-time application data. You can create and view charts and dashboards in the Atlas Portal, and embed these in your web and mobile apps.

![Example: Product sales](images/charts.png)

# Online archive

In many real life use cases data ages over time.

![Example: Automatically offload 'old' digital receipts](images/OnlineArchive.png)

<!--TODO:
# Search
# Data Lake
-->
from pymongo import MongoClient
import random
import os

# See README.md regarding exporting Atlas connection string to an envrionment variable
mongodb_uri = os.getenv('mongodb_uri')
client = MongoClient(mongodb_uri)
db = 'shopper'
col = 'orders'
orders = client[db][col]

# A filter just querying the data at a random location roughly in the Netherlands.
# Could use any other query to filter the data.
filter={'geometry': {'$geoWithin': {'$centerSphere': [[random.randint(5000,6000)/1000, random.randint(51700,52800)/1000], .01]}}}

# number of matches
count = orders.count_documents(filter)
print()
print(filter)
print()
if count > 0:
    # retrieve one document
    result = orders.find_one(filter=filter)
    print(result)
    print()
    print('Printed one matching document out of',count,'results')
    print()
else:
    print('Query yielded no results')
    print()

from pymongo import MongoClient
import random
import os

# See README.md regarding exporting Atlas connection string to an envrionment variable
# local:    mongodb://localhost:27017/shopper
# Atlas:    mongodb+srv://<user>:<pass>@customer-tech-2022.mz3yq.mongodb.net/shopper
atlas_uri = os.getenv('atlas_uri')
client = MongoClient(atlas_uri)
db = client.shopper

# A filter just querying the data at a random location in the Netherlands.
# Could use any other query to filter the data.
filter={'geometry': {'$geoWithin': {'$centerSphere': [[random.randint(5000,6000)/1000, random.randint(51700,52800)/1000], .001]}}}

# number of matches
count = db.order.count_documents(filter)
# retrieve document(s)
result = db.order.find_one(filter=filter)

print()
print(filter)
print()
if count > 0:
    print(result)
    print()
    print('Printed a matching document out of',count,'results')
    print()
else:
    print('Query yielded no results')
    print()

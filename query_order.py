from pymongo import MongoClient
import random
import os

# local
client = MongoClient('mongodb://localhost:27017/shopper')

# See README.md regarding exporting Atlas connection string to an envrionment variable
atlas_uri = os.getenv('atlas_uri')
client = MongoClient(atlas_uri)

db = client.shopper

# A filter just querying the data at a random location in the Netherlands.
# Could use any other query to filter the data.
filter={
    'geometry': {
        '$geoWithin': {
            '$centerSphere': [
                [
                    random.randint(5000,6000)/1000, random.randint(51700,52800)/1000
                ], .001
            ]
        }
    }
}

count = db['order'].count_documents(filter) # number of matches
result = db['order'].find(filter=filter) # cursor with documents

if count > 0:
    print(result[0])
    print('Printed first document out of',count,'results')
else:
    print('Query yielded no results')
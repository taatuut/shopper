from pymongo import MongoClient
import random

# local
client = MongoClient('mongodb://localhost:27017/shopper')

# Atlas - example dummy connection string:
#
#       "mongodb+srv://<user>:<pass>@yourserver.at.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#

# Replace <user> and <pass>, and 'myFirstDatabase' with the name of the database that teh connections should use by default.
# You can find the connection string in the Atlas UI. You can leave out the Pymongo prefix.
# TODO: replace YOUR_CONNECTION_STRING_HERE with your own Atlas connection string for Python in the next line and uncomment.
#client = MongoClient(<YOUR_CONNECTION_STRING_HERE>)

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
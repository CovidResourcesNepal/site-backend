import pymongo
from Server import settings as ss
from Server import dbSecret
from service.sheet_script import get_json

# Connect to mongodb test database
client = pymongo.MongoClient(dbSecret.URI_CONNECTION_STRING)
db = client.covidResources


def get_collection(type_):
    '''
    :return: List of all the items in the collection `type_` in the database
    '''
    collection = db[type_]
    cursor = collection.find()
    items = list(cursor)
    [item.pop('_id', None) for item in items]
    return items

def drop_fundraisers():
    db.fundraisers.drop()

def delete_fundraisers(ids):
    fundraisers = db.response
    try:
        for id in ids:
            fundraisers.remove(ObjectId(id))
        return 'success'
    except Exception as e:
        return 'error', e

def reset_collection(type_):
    data = get_json(type_)
    db[type_].drop()
    for row in data:
        db[type_].insert_one(row)

def reset_fundraisers():
    fundraisers = get_json('fundraisers')
    drop_fundraisers()
    fundraisers_db = db.fundraisers
    for fundraiser in fundraisers:
        fundraisers_db.insert_one(fundraiser)

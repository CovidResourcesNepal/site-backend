import pymongo
from Server import settings as ss
from Server import dbSecret
from service.sheet_script import get_fundraisers_json

# Connect to mongodb test database
client = pymongo.MongoClient(dbSecret.URI_CONNECTION_STRING)
db = client.covidResources


def get_fundraisers():
    '''
    :return: List of all the fundraisers in database
    '''
    fundraisers = db.fundraisers
    cursor = fundraisers.find()
    campaigns = list(cursor)
    [item.pop('_id', None) for item in campaigns]
    return campaigns

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

def reset_fundraisers():
    fundraisers = get_fundraisers_json()
    drop_fundraisers()
    fundraisers_db = db.fundraisers
    for fundraiser in fundraisers:
        fundraisers_db.insert_one(fundraiser)

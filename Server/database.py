import os
import pymongo
from Server import settings as ss
from Server import db_secret
from Server import static_path
from service.sheet_script import get_fundraisers_json
from bson.json_util import dumps
from bson.objectid import ObjectId
from collections import Counter

DATABASE_ADDRESS = os.environ.get('DATABASE_ADDRESS')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_ADMIN = os.environ.get('DATABASE_ADMIN')
DATABASE_PWD = os.environ.get('DATABASE_PWD')

# Connect to mongodb test database
client = pymongo.MongoClient(
    host=DATABASE_ADDRESS or ss.DATABASE_ADDRESS,
    port=DATABASE_PORT or ss.DATABASE_PORT,
    username=DATABASE_ADMIN or db_secret.DATABASE_ADMIN,
    password=DATABASE_PWD or db_secret.DATABASE_PWD,
    authMechanism='SCRAM-SHA-256')
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

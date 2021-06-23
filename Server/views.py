from Server import app
from flask import request, jsonify, render_template
from flask_cors import CORS
from Server import database
import os
import subprocess

CORS(app)

@app.route('/api/<type_>', methods=['GET'])
def food(type_):
    '''
    The api endpoint for all food resources
    '''
    collection = database.get_collection(type_)
    print(collection)
    return jsonify(collection), 200
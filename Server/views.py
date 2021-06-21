from Server import app
from flask import request, jsonify, render_template
from flask_cors import CORS
from Server import database
import os
import subprocess

CORS(app)

@app.route('/api/fundraisers', methods=['GET'])
def api():
    '''
    The api endpoint for all fundraisers
    '''
    fundraisers = database.get_fundraisers()
    print(fundraisers)
    return jsonify(fundraisers), 200

# @app.route("/pull")
# def pull():
#     os.chdir('/home/ubuntu/ny-exhibition')
#     subprocess.run(['git', 'reset', '--hard', 'HEAD'])
#     response = subprocess.check_output(['git','pull'])
#     subprocess.run(['touch', 'client.wsgi'])
#     return response

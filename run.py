import sys
import os
CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
sys.path.append(CURRENT_DIR)

from Server import app
import Server.views
from Server.settings import SERVER_HOST, SERVER_PORT

# start flask service
if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, threaded=True)
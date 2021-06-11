from flask import Flask
import os

project_root = os.path.dirname(__file__)
static_path = os.path.abspath(os.path.join(project_root, '..', 'static'))

app = Flask(__name__, static_folder=static_path)
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/work-watch"
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/projects", methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        return create_project(request.data)
    else:
        return get_projects()

def get_projects():
    projects = mongo.db.projects.find({})
    return dumps(projects)

def create_project(body):
    body = json.loads(body)
    result = mongo.db.projects.insert_one(body)
    return { "name": body["name"], "color": body["color"] }

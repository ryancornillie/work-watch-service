from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json
from flask import request
from flask_cors import CORS
from datetime import datetime
import uuid

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
    body["id"] = str(uuid.uuid4())
    body["record_id"] = None
    result = mongo.db.projects.insert_one(body)
    return { "name": body["name"], "color": body["color"], "id": body["id"]}

def update_current_project_record(project_id, record_id):
    result = mongo.db.projects.update_one({"id": project_id},
     { "$set": { "record_id": record_id }})


@app.route("/records", methods=['GET', 'POST', 'PATCH'])
def records():
    if request.method == 'POST':
        return create_record(request.data)
    elif request.method == 'PATCH':
        return update_record(request.data)

def create_record(body):
    body = json.loads(body)
    record_entry = {
        "project_id" : body["project_id"],
        "start_time" : datetime.now(),
        "end_time" : None,
        "id" : str(uuid.uuid4())
    }
    print("entry", record_entry)
    result = mongo.db.records.insert_one(record_entry).inserted_id

    if (result):
        #TODO: this will be handled in seperate put request
        update_current_project_record(record_entry["project_id"], record_entry["id"])   

    #TODO: handle error here

    return { "project_id": record_entry["project_id"],
     "start_time": record_entry["start_time"], "id": record_entry["id"] }

def update_record(body):
    body = json.loads(body)
    body["end_time"] = datetime.now()
    result = mongo.db.records.update_one({"id": body["id"]}, { "$set": { "end_time": body["end_time"]} })
    return body


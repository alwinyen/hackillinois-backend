from flask import Flask, json, request
from flask_cors import CORS
from Database import Database
from googlesearch import search
import jwt
import sys
from bson.objectid import ObjectId

testURL = "https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html"
dbURL = "mongodb+srv://danielchen:CFDl0VIM7HIQHwpL@cluster0-5ytij.mongodb.net/test?retryWrites=true&w=majority"
SECRET = 'secret'

def runDB():
    db = Database(dbURL)

def getToken(userID):
    encoded_jwt = jwt.encode({"userID": str(userID)}, SECRET, algorithm='HS256')
    return {
        "token": encoded_jwt.decode('ascii'),
        "status": "SUCCESS"
    }

def server():
    api = Flask(__name__)
    CORS(api)

    db = Database(dbURL)

    @api.route('/register', methods=['POST'])
    def register():
        username = request.args['username']
        password = request.args['password']
        name = request.args['name']

        if (db.findUser(username)):
            return {
                "status" : "ERROR",
                "msg" : "username already exists"
            }
        else:
            id = db.insertUser(username, password, name)

            return getToken(username)

    @api.route('/login', methods=['POST'])
    def login():
        username = request.args['username']
        password = request.args['password']

        user = db.authUser(username, password)
        if (user.count() > 0):
            print(user[0])
            return getToken(user[0]['_id'])

        return {
            "status" : "ERROR",
            "msg" : "login credentials incorrect"
        }

    @api.route('/add_favorite', methods=['POST'])
    def add_favorite():
        if 'token' not in request.args:
            return {
                "status" : "ERROR",
                "msg" : "not logged in"
            }

        sourceID = request.args['sourceID']
        status = request.args['status'] == '1'

        db.favoriteSource(sourceID, status)
        print(status)

        return {
            "status" : "SUCCESS"
        }


    @api.route('/get_favorite', methods=['POST'])
    def get_favorite():
        if 'token' not in request.args:
            return {
                "status" : "ERROR",
                "msg" : "not logged in"
            }

        token = request.args['token']
        payload = jwt.decode(token, SECRET, algorithms='HS256')
        userID = payload['userID']

        return json.dumps(db.getFavorite(userID))

    @api.route('/api', methods=['POST'])
    def query():
        query = request.args['query']
        num = int(request.args['num'])

        urls = search(query, tld='com', lang='en', num=num, start=0, stop=num, pause=0.1)

        sources = []
        for url in urls:
            source = db.insertSource(url)
            sources.append({
                "data" : source.getDict(),
                "sourceID" : source._id
            })

        if 'token' in request.args:
            token = request.args['token']
            payload = jwt.decode(token, SECRET, algorithms='HS256')
            userID = payload['userID']
            for source in sources:
                db.addSourceToUser(userID, source['sourceID'])

        return {
            "sources" : sources,
            "status" : "SUCCESS"
        }


    if len(sys.argv) > 1:
        api.run(host='0.0.0.0', debug=False)
    else:
        api.run()

if __name__ == '__main__':
   server()
from flask import Flask, json, request
from flask_cors import CORS
from Database import Database
from googlesearch import search
import jwt
import sys
from urllib.parse import urlparse
import traceback

import time

testURL = "https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html"
dbURL = "mongodb+srv://danielchen:CFDl0VIM7HIQHwpL@cluster0-5ytij.mongodb.net/test?retryWrites=true&w=majority"
SECRET = 'secret'

blacklist = []
with open('blacklist.txt', 'r') as f:
    blacklist = f.read().split('\n')

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
        try:
            payload = jwt.decode(token, SECRET, algorithms='HS256')
            userID = payload['userID']

            return json.dumps(db.getFavorite(userID))
        except:
            return {
                "status" : "ERROR",
                "msg" : "invalid token"
            }

    @api.route('/get_sorted', methods=['POST'])
    def get_sorted():
        if 'token' not in request.args:
            return {
                "status" : "ERROR",
                "msg" : "not logged in"
            }

        token = request.args['token']
        try:
            payload = jwt.decode(token, SECRET, algorithms='HS256')
            userID = payload['userID']
            print(db.getSortedFavorites(userID))
            return json.dumps(db.getSortedFavorites(userID));
        except:
            return {
                "status" : "ERROR",
                "msg" : "invalid token"
            }


    @api.route('/api', methods=['POST'])
    def query():
        query = request.args['query']
        num = int(request.args['num'])

        print(query)

        timer = time.time()

        def getGoogleSearch(query, n, start=0):
            urls = search(query, tld='com', lang='en', num=n, start=start, stop=n, pause=0.01)
            invalid = 0
            valid = []

            for url in urls:
                print(url)
                if urlparse(url).netloc in blacklist:
                    invalid += 1
                else:
                    try:
                        source = db.insertSource(url)
                        valid.append(source)
                    except:
                        invalid += 1

            if invalid == 0:
                return valid

            valid += getGoogleSearch(query, invalid, start + n)

            return valid

        sources = getGoogleSearch(query, num)
        print(sources)

        # sources = []
        # for url in urls:
        #     try:
        #         source = db.insertSource(url)
        #         sources.append(source)
        #     except AttributeError as err:
        #         traceback.print_exc()

        if 'token' in request.args:
            token = request.args['token']
            try:
                payload = jwt.decode(token, SECRET, algorithms='HS256')
            except:
                return {
                    "status" : "ERROR",
                    "msg" : "invalid token"
                }
            userID = payload['userID']
            for source in sources:
                db.addSourceToUser(userID, source['_id'])

        print("total search time:" + str(time.time() - timer))

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
from flask import Flask, json, request
from flask_cors import CORS
from Database import Database
from googlesearch import search
import jwt
import sys

testURL = "https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html"
dbURL = "mongodb+srv://danielchen:CFDl0VIM7HIQHwpL@cluster0-5ytij.mongodb.net/test?retryWrites=true&w=majority"
SECRET = 'secret'

def runDB():
    db = Database(dbURL)

def getToken(username):
    encoded_jwt = jwt.encode({"username": username}, SECRET, algorithm='HS256')
    print(encoded_jwt.decode('ascii'))
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

        if (db.authUser(username, password)):

            return getToken(username)

        return {
            "status" : "ERROR",
            "msg" : "login credentials incorrect"
        }

    @api.route('/api', methods=['POST'])
    def query():
        query = request.args['query']
        num = int(request.args['num'])
        token = request.args['token']

        urls = search(query, tld='com', lang='en', num=num, start=0, stop=num, pause=0.1)

        sources = []
        for url in urls:
            print(url)
            source = Database.Source(url)
            sources.append(source.getDict())

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
from flask import Flask, json, request
from Database import Database
from googlesearch import search

testURL = "https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html"
dbURL = "mongodb+srv://danielchen:CFDl0VIM7HIQHwpL@cluster0-5ytij.mongodb.net/test?retryWrites=true&w=majority"

def runDB():
    db = Database(dbURL)

def server():
    api = Flask(__name__)

    @api.route('/api', methods=['POST'])
    def query():
        query = request.args['query']
        num = int(request.args['num'])

        urls = search(query, tld='com', lang='en', num=num, start=0, stop=num, pause=0.1)

        sources = []
        for url in urls:
            print(url)
            source = Database.Source(url)
            sources.append(source.getDict())

        return json.dumps(sources)


    # api.run(host='0.0.0.0', debug=False)
    api.run()

if __name__ == '__main__':
   server()
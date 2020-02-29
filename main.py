from flask import Flask, json, request
from Database import Database
testURL = "https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html"
dbURL = "mongodb+srv://danielchen:CFDl0VIM7HIQHwpL@cluster0-5ytij.mongodb.net/test?retryWrites=true&w=majority"

def runDB():
    db = Database(dbURL)

def server():
    api = Flask(__name__)

    data = {
        "field1" : 1
    }

    @api.route('/test', methods=['GET'])
    def get_shit():
        return json.dumps(data)

    @api.route('/post', methods=['POST'])
    def post_shit():
        print(request.args)
        return data

    api.run(host='0.0.0.0', debug = False);

def dns():
    dns_class = sewer.CloudFlareDns(CLOUDFLARE_EMAIL='leechangwook0621@gmail.com',
                                    CLOUDFLARE_API_KEY='04q_Hm-x68WcJviMo8gdXsCBvYq7HieRukh_hdzw')
    client = sewer.Client(domain_name='www.idisaster.com',
                          dns_class=dns_class)
    certificate = client.cert()
    certificate_key = client.certificate_key
    account_key = client.account_key

if __name__ == '__main__':
    server()
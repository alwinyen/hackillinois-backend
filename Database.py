import pymongo
from ArticleScraper import getArticle, summarize
from CitationGeneration import getCitation
from bson.objectid import ObjectId

class Database:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client['HackIllinois2020_working']
        # self.insertUser("test", "test", "test")
        # self.insertSource("https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html")

    def insertUser(self, username, password, name):
        user = self.User(username, password, name)
        self.db['User'].insert_one(user.getDict())

    def findUser(self, username):
        user = self.db['User'].find({
            "username" : username
        })
        return user.count() > 0

    def authUser(self, username, password):
        user = self.db['User'].find({
            "username" : username,
            "password" : password
        })
        return user

    def addSourceToUser(self, userID, sourceID):
        self.db['User'].update({
            '_id' : ObjectId(userID)
        }, {
            '$push' : {'sources' : ObjectId(sourceID)}
        })

    def insertSource(self, url):
        source = self.Source(url)
        id = self.db['Source'].insert_one(source.getDict())
        source = source.getDict()
        source['_id'] = str(id.inserted_id)
        return source

    def favoriteSource(self, sourceID, status):
        source = self.db['Source'].update({
            '_id' : ObjectId(sourceID)
        }, {
            '$set' : {'favorite' : status}
        })

    def getFavorite(self, userID):
        user = self.db['User'].find_one({
            "_id" : ObjectId(userID)
        })

        sourceIDs = user['sources']

        sources_cursor = self.db['Source'].find({
            '$and' : [
                {'_id' : {'$in' : sourceIDs}},
                {'favorite' : True}
            ]
        })

        sources = []
        for source in sources_cursor:
            source['_id'] = str(source['_id'])
            sources.append(source)

        return sources

    def insertMindmapNode(self, sourceID):
        mindmapNode = self.MindmapNode(sourceID)
        self.db['MindmapNode'].insert_one(mindmapNode.getDict())

    def insertMindmap(self, name):
        mindmap = self.Mindmap(name)
        self.db['Mindmap'].insert_one(mindmap)

    class User:
        def __init__(self, username, password, name):
            self.id = -1
            self.username = username
            self.password = password
            self.name = name
            self.mindmaps = []
            self.sources = []

        def getDict(self):
            return {
                "username" : self.username,
                "password" : self.password,
                "name" : self.name,
                "mindmaps" : self.mindmaps,
                "sources" : self.sources
            }

    class Source:
        def __init__(self, url):
            self.url = url

            self.citation = getCitation(self.url)

            article = getArticle(self.url)
            self.title = article.title

            summary = summarize(article)
            self.text = summary

            self.favorite = False;

        def getDict(self):
            return {
                "url" : self.url,
                "title" : self.title,
                "citation" : self.citation,
                "text" : self.text,
                "favorite" : self.favorite
            }

    class MindmapNode:
        def __init__(self, sourceID):
            self.sourceID = sourceID
            self.connections = []

        def getDict(self):
            return {
                "sourceID" : self.sourceID,
                "connections" : self.connections
            }

    class Mindmap:
        def __init__(self, name):
            self.name = name
            self.nodes = []

        def getDict(self):
            return {
                "name" : self.name,
                "nodes" : self.nodes
            }

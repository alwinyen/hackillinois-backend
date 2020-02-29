import pymongo
from ArticleScraper import getArticle, summarize
from CitationGeneration import getCitation

class Database:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client['HackIllinois2020_working']
        # self.insertUser("test", "test", "test")
        self.insertSource("https://www.cnn.com/2020/02/29/health/us-coronavirus-saturday/index.html")

    def insertUser(self, username, password, name):
        user = self.User(username, password, name)
        self.db['User'].insert_one(user.getDict())

    def insertSource(self, url):
        source = self.Source(url)
        self.db['Source'].insert_one(source.getDict())

    def insertMindmapNode(self, sourceID):
        mindmapNode = self.MindmapNode(sourceID)
        self.db['MindmapNode'].insert_one(mindmapNode.getDict())

    def insertMindmap(self, name):
        mindmap = self.Mindmap(name)
        self.db['Mindmap'].insert_one(mindmap)

    class User:
        def __init__(self, username, password, name):
            self.id = -1;
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

import dbparams
from pymongo import MongoClient
from bson.objectid import ObjectId


class DAO(object):
	dbClient = MongoClient(host=dbparams.mongodb['host'], port=dbparams.mongodb['port'])
	db = dbClient[dbparams.mongodb['db']]

	def __init__(self, collection):
		self.collection = collection

	def dbConnTest(self):
		print(self.db.command("serverStatus"))

	def create(self, entity):
		response = self.db[self.collection].insert_one(entity)
		return response

	def batchCreate(self, entities):
		response = self.db[self.collection].insert_many(entities)
		return

	def retrieve(self, query):
		response = self.db[self.collection].find(filter=query)
		return response

	def retrieveFirst(self, query):
		response = self.db[self.collection].find_one(filter=query)
		return response

	def retrieveByID(self, id):
		return self.retrieveFirst({'_id': ObjectId(str(id))})

	def update(self, updateSet, where):
		return

	def updateByID(self, updateSet, id):
		return

	def delete(self, where):
		return

	def deleteByID(self, id):
		return

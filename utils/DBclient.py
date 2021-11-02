import pymongo
from bson.objectid import ObjectId
import sys
sys.path.append('..')
from main import app

class MongoConnection:
	def __init__(self, collection):
		self.db_url = app.config['SAVE_PATH'] if app.config['SAVE_PATH'].startswith('mongodb') else 'mongodb://localhost:27017'
		self.db_name = 'store'
		self.col_name = collection
		self.user_name = 'pyclient'
		self.user_pwd = 'password'
		self.client = pymongo.MongoClient(
			self.db_url,
			socketTimeoutMS=5000
			)
		self.db = self.client[self.db_name]
		self.db.authenticate(self.user_name, self.user_pwd)
		self.collection = self.db[self.col_name]

	def __enter__(self):
		return  self.collection

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.client.close()


if __name__ == '__main__':

	with MongoConnection('test') as conn:
		file_dict = {
		    "filename":"wahaha",
		    "filesize":100,
		    "DateTime":"2021-11-19 00:00:00"
			}

		res = conn.insert(file_dict)
		print(res)

		q = {'filename':'wahaha'}
		res = conn.find(q)
		print(list(res))

		res = conn.drop()
		print(res)
       

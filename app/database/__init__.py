from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

from app.config import config

username = quote_plus(config.MONGO_USERNAME.get_secret_value())
password = quote_plus(config.MONGO_PASSWORD.get_secret_value())
cluster = config.MONGO_CLUSTER.get_secret_value()

uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '/?retryWrites=true&w=majority'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database = client.get_database('test')

# if __name__ == "__main__":
#     print(client)
#     print(database)
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pathlib import Path

env_path = Path('implement-RAG/graph-rag-system/src/.env')
# load_dotenv(dotenv_path=env_path)
# uri = os.getenv("MONGO_URI")
# print(uri)

uri = "mongodb+srv://nimishkumar0305:nimish0305@pinewheel.jtw34.mongodb.net/?retryWrites=true&w=majority&appName=pinewheel"
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
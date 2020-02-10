import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


API_PORT = int(os.environ.get('API_PORT', 8888))
DATASET_PATH = os.environ.get('DATASET_PATH')
DATASET_FILENAME = os.environ.get('DATASET_FILENAME')
GRAPH_FILENAME = os.environ.get('GRAPH_FILENAME')

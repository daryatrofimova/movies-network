
Using the movies dataset from Kaggle, return Bacon number or  number of connecting actors between any two actors and their full connection path.


* How to use:

Download https://www.kaggle.com/rounakbanik/the-movies-dataset/data and set it as your DATASET_PATH 
(either in .env or as DATASET_PATH=/some/path python api.py)

First startup time is ~2 minutes, after that preprocessed dataset and graph are stored in DATASET_PATH directory.


* How to start the server:

DATASET_PATH=/some/path python api.py

There is a swagger ui available at http://localhost:8888.

* Description:

The movies dataset is converted into a graph that connects two actors if they appear together in a movie.
Bacon number /  connecting actors number is calculated as shortest path between two actors 
using python networkx implementation of Dijkstra algorithm.


* Known issues:

1) Returns a generic error if one of the actors is not present in the graph
2) Returns a generic error if there is no path between two actors


* Notes

RESTful API is implemented with Sanic, a high performance async web framework.
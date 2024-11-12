from flask import Flask, request, jsonify
import networkx as nx
from pymongo import MongoClient
import chromadb
import json

# Initialize Flask app
app = Flask(__name__)

# Set up MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["network_graph_db"]
graphs_collection = db["graphs"]

# Set up Chroma DB connection
client = chromadb.Client()
collection_chroma = client.get_or_create_collection("network_graph_collection")

# Create a graph object (use NetworkX or any other method to create your graph)
def create_or_update_graph(graph_id, data):
    graph = nx.Graph()
    for node in data['nodes']:
        graph.add_node(node['id'], **node['attributes'])
    for edge in data['edges']:
        graph.add_edge(edge['source'], edge['target'], **edge['attributes'])

    # Store graph data in MongoDB
    graphs_collection.update_one(
        {"graph_id": graph_id},
        {"$set": {"graph_data": json.dumps(nx.node_link_data(graph))}},
        upsert=True
    )

    # You can also update Chroma DB here by adding embeddings for the graph nodes
    for node in graph.nodes(data=True):
        # Create embeddings and add to Chroma DB (You can use your existing embedding generation logic)
        node_embedding = [0.0]  # Example: Replace with real embedding logic
        node_text = str(node[1])  # Example: Replace with real text for embedding

        collection_chroma.add(
            documents=[node_text],
            metadatas=[{"node_id": node[0]}],
            embeddings=[node_embedding],
            ids=[str(node[0])]  # Use node ID as Chroma DB's ID
        )

    return graph

# API endpoint to create or update a graph
@app.route("/api/graph", methods=["POST"])
def create_graph():
    try:
        data = request.json
        graph_id = data["graph_id"]
        graph_data = data["data"]
        
        # Create or update the graph in MongoDB and Chroma DB
        graph = create_or_update_graph(graph_id, graph_data)
        
        return jsonify({"status": "success", "message": "Graph created/updated successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# API endpoint to fetch a graph by graph_id
@app.route("/api/graph/<graph_id>", methods=["GET"])
def get_graph(graph_id):
    try:
        # Fetch graph data from MongoDB
        graph_data = graphs_collection.find_one({"graph_id": graph_id})
        
        if not graph_data:
            return jsonify({"status": "error", "message": "Graph not found."}), 404
        
        graph = nx.node_link_graph(json.loads(graph_data["graph_data"]))
        return jsonify({"status": "success", "graph": nx.node_link_data(graph)}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500)
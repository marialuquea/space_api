from flask import Flask, request, Response
from flask_restful import Resource, Api
from qa_text import get_document_store, get_retriever, get_reader, create_pipeline, ask_question


app = Flask(__name__)
api = Api(app)

# initialise document store
document_store = get_document_store()

# get retrievers
retriever1, retriever2 = get_retriever(document_store)

# get reader
reader = get_reader()

# combine them into a pipeline
pipeline = create_pipeline(reader, retriever2)

@app.route('/initialized', methods=['GET'])
def respond():
    return Response("yes it works", status=201)

@app.route('/query', methods=['POST'])
def query():

    print(request.args)
    # req: {'query': "What's the capital of France?", 'params': {'filters': {}, 'Retriever': {'top_k': 3}, 'Reader': {'top_k': 3}}}
    
    # ask_question(pipeline, question)

    return Response("WOOP WOOP", status=201)
    

class Ping(Resource):
    def get(self):
        return 'pong', 200 

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h2>Maria Luque Anguita - Space diss</h2>"

api.add_resource(Ping, '/ping')


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True) 


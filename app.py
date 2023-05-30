import openai
import random
import json
from elasticsearch import Elasticsearch

# Replace with your API key
openai.api_key = "your_openai_api_key_here"

from elasticsearch import Elasticsearch

# Replace with your Elasticsearch credentials and host details
from flask import Flask, render_template, request, jsonify
import threading

app = Flask(__name__)

# Initialize variables for Elasticsearch and OpenAI clients
es = None
openai.api_key = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['POST'])
def config():
    global es, openai
    openai.api_key = request.form['openai_key']
    es_host = request.form['es_host']
    es_port = int(request.form['es_port'])
    es_username = request.form['es_username']
    es_password = request.form['es_password']

    es = Elasticsearch(
        [{"host": es_host, "port": es_port, "scheme": "https"}],
        http_auth=(es_username, es_password),
    )

    return jsonify({'success': True})

@app.route('/message', methods=['POST'])
def message():
    if not es or not openai.api_key:
        return jsonify({'error': 'Configuration is missing. Please provide the OpenAI API key and Elasticsearch details.'}), 400

    user_input = request.form['user_input']
    response = elastic_request(user_input)
    return jsonify({'response': response})


def elastic_request(user_input):
    
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "text_expansion": {
                            "ml.tokens": {
                                "model_id": ".elser_model_1",
                                "model_text": "{}".format(user_input)
                            }
                        }
                    }#,
                    #{
                    #    "range" : {
                    #        "timestamp" : {
                    #            "gte" : "now-128h",
                    #            "lte" : "now"
                    #        }
                    #    }
                    #}
                ]
            }
        },
        "size": 3,
        "sort": [
            {
                "_score": {
                    "order": "desc"
                }
            }
        ]
    }


    search_results = es.search(body=body)

    top_result = search_results["hits"]["hits"][0]["_source"]["text_field"] if search_results["hits"]["hits"] else "No results found."
    second_result = search_results["hits"]["hits"][1]["_source"]["text_field"] if search_results["hits"]["hits"] else "No results found."
    print(top_result)
    print(second_result)

    analysis_input = f"With the following user input {user_input} please analyze the following two log messages: {top_result} AND {second_result}"
    analysis=[{"role": "system", "content": "You are a Site Reliability Engineer, please review logs messages and suggest the root cause."},
              {"role": "user", "content": analysis_input}]
    analysis_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=analysis,
        temperature=0,
    ) 
    print(analysis_response)
    analysis = analysis_response["choices"][0]["message"]["content"].strip()

    return analysis


if __name__ == "__main__":

    app.run(host="localhost", port=8080, debug=True)

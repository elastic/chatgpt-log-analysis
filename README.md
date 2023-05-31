# Log Analyzer with OpenAI and Elasticsearch

This project is a log analyzer built on Flask, powered by the OpenAI GPT-4 model and Elasticsearch powered by ESRE. You will need to setup your Elasticsearch environment to use ESRE for this to work.

It takes a user input, queries Elasticsearch for relevant log messages, and then uses the OpenAI model to analyze these logs and provide suggestions about the root cause of any identified issues.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

- Here is an archiecture diagram of how this works.
![alt text](https://github.com/davidgeorgehope/ChatGPT4ElasticAgents/blob/main/architecture.png)

### Prerequisites

- Python 3.6 or higher
- Elasticsearch setup (v7.x preferred)
- OpenAI API key

### Installation

1. Clone the repository to your local machine:
        ```
        git clone https://github.com/elastic/chatgpt-log-analysis
        cd chatgpt-log-analysis
        ```
2. Install the required Python packages using pip:

        ```
        pip install -r requirements.txt
        ```

Note: If you have both Python 2 and Python 3 installed on your machine, you may need to use `pip3` instead of `pip`.

The `requirements.txt` file includes the following packages:

- flask
- openai
- elasticsearch

3. Run the application:

        ```python app.py```

Again, you may need to use `python3` instead of `python`, depending on your setup.

### Usage

After starting the Flask app, you can use the following endpoints:

- `/` : Returns the 'index.html' page. This is where you should start. 

- `/config` (POST method): Configures the Elasticsearch and OpenAI clients. The request should contain the following parameters in form data, you can use the front end application and the "Save Config" button to populate this:

    - 'openai_key' : Your OpenAI API key.
    - 'es_host' : Host of the Elasticsearch instance.
    - 'es_port' : Port number of the Elasticsearch instance.
    - 'es_username' : Username for Elasticsearch instance.
    - 'es_password' : Password for Elasticsearch instance.

- `/message` (POST method): Takes 'user_input' as a form data parameter, queries Elasticsearch with the input, analyzes the top two log results using OpenAI's GPT-4 model, and returns the analysis.

### Troubleshooting

If the `/message` endpoint returns an error message saying "Configuration is missing. Please provide the OpenAI API key and Elasticsearch details.", make sure you have properly configured the Elasticsearch and OpenAI clients using the `/config` endpoint.

### Further Development

This is a basic setup for a log analysis tool. Depending on your specific use case and needs, you may want to modify the Elasticsearch query, tune the OpenAI model parameters, or handle more complex log analysis tasks.

Please feel free to fork this project and modify it according to your needs.

## Disclaimer
See the full documentation online in this [Elastic Blog Post] (https://www.elastic.co/blog/kubernetes-errors-elastic-observability-logs-openai). https://github.com/elastic/chatgpt-error-analysis is an Elastic Labs project. Elastic Labs projects are for illustrative and experimental purposes only. This Elastic Labs project is not part of any product or services offering provided or supported under a commercial license or subscription. This project is made available as-is under the terms of the license associated with this project. The release and timing of any features or functionality described in this project remain at Elastic's sole discretion. Any features or functionality not currently available may not be delivered on time or at all.

## License
elastic/chatgpt-log-analysis is available under the Apache 2.0 license. For more details see LICENSE.



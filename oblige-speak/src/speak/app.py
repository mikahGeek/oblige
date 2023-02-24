from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
import os
import sys
import openai
import json
import db

logger = Logger(service="APP")
tracer = Tracer(service="APP")
metrics = Metrics(namespace="MyApp", service="APP")
app = ApiGatewayResolver()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/speak")
@tracer.capture_method
def speak():
  # return openai's response to the 'text' field
  input = app.current_event.json_body['text'];
  id = db.log_request(input);
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=generate_prompt(input),
    temperature=0,
    max_tokens=1500
  )
  text = '';
  for choice in response.choices:
    text = choice.text + ' ';
  db.log_response(text, id)
  return text;

def generate_prompt(input):
    return """
      Text: {}
      Responses:""".format( input.capitalize() )

@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise

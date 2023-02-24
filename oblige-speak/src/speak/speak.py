import os
import sys
import openai
import json
from flask import Flask, redirect, render_template, request, url_for, jsonify
import logging

from requestlog import log_request, log_response

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/speak", methods=(["POST"]))
def speak():
  # return openai's response to the 'text' field
  input = request.get_json()['text'];
  id = log_request(input);
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=generate_prompt(input),
    temperature=0,
    max_tokens=1500
  )
  text = '';
  for choice in response.choices:
    text = choice.text + ' ';
  log_response(text, id)
  return text;

def generate_prompt(input):
    return """
      Text: {}
      Responses:""".format( input.capitalize() )

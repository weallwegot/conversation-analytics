from flask import Flask, request, url_for, render_template
from flask import jsonify, session, current_app
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import random
from textblob import TextBlob
import json
import requests

#literally should need none of these imports except
#script 
#userinfo
#flask
#database
#json
#uuid
#datetime

from datetime import datetime
import simplejson as json
import uuid

app = Flask(__name__)
app.secret_key = "2"
#api
api = Api(app)
#cors for cross origin headers 
CORS(app)


@app.route('/')
def fresh_session():
    return render_template('index.html')




if __name__ == "__main__":
    app.run()
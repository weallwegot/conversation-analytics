from flask import Flask, request, url_for, render_template
from flask import jsonify, session, current_app
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import random
from textblob import TextBlob
import json
import requests
import os


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

from analyze import analyze_text_conversation

app = Flask(__name__)
app.secret_key = "2"
#api
api = Api(app)
#cors for cross origin headers 
CORS(app)




@app.route('/')
def fresh_session():
	# check for config file
	paths_to_files = []
	results = {}

	# if config doesnt exist, render input page
	try:
		config = json.load(open("config.json"))
		critical_numbers = config["critical numbers"]
		for n in critical_numbers:
			num = n.replace('(','').replace(')','')
			if len(num) == 10:
				num = "+1"+num
			elif len(n) == 12:
				num = num
			else:
				raise Exception('Invalid number entered!')
			# TODO: refine this path more generally
			p = os.path.abspath('../../../Downloads/baskup-master/'+num)
			for i in os.walk(p):
				for e in i:
					for entry in e:
						if ('iMessage' in entry) and ('.txt' in entry):
							file_name = entry
							break
			path = p + os.sep + file_name
			paths_to_files.append(path)
			res = analyze_text_conversation(path)
			results[num] = res
			print "*****" + num + "*****"
			print res



			


	except:
		render_template('settings.html')

	# if config exists, render data page
	return render_template('index.html')




if __name__ == "__main__":
    app.run()
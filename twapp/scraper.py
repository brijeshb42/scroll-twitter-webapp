from flask import Flask, Blueprint, request, jsonify
import link_parser as lp

scraper_app = Blueprint('scraper',__name__)

"""
Endpoint to retrive title and description of a url and send a json response
"""
@scraper_app.route('/')
def get_data():
	url = request.args.get('url',None)
	if url is not None and url is not '':
		title, desc, typ = lp.get_data(url)
		return jsonify(title= title, desc= desc, type=typ)
	else:
		return jsonify(type='error', title='Invalid Url')
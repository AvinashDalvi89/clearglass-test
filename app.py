#!/usr/bin/env python
"""
    File 	        : app.py
    Package         :
    Description     : This Flask API allow to get cost details by client/project/cost type wise.
    Project Name    : FLASK REST API
    Created by Avinash on 02/02/2020
"""

from flask import Flask, request, jsonify, make_response, render_template
import traceback
from cost_explorer_controller import *


app = Flask(__name__)

def index(path=None):
    return render_template('/index.html', path=path)

path = '/'
app.add_url_rule(path, 'index', index)


@app.route('/api/v1.0/cost-explorer', methods=['GET'])
def get_cost_explorer():

    clients = request.args.getlist('clients[]')
    projects = request.args.getlist('projects[]')
    cost_types = request.args.getlist('cost_types[]')
    print_log = request.args.get('print_log')

    obj = CostExplorerController(print_log)
    result = obj.get_details(clients, projects,cost_types)
    return make_response(jsonify(result))

# this is to throw error which method is allow
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return make_response(jsonify({'error': 'Path Not found','status': 404}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not found','status': 405}), 405)



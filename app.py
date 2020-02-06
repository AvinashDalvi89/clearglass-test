#!/usr/bin/env python
"""
    File 	        : app.py
    Package         :
    Description     :
    Project Name    : FLASK REST API
    Created by Avinash on 02/02/2020
"""

from flask import Flask, request, jsonify, make_response
import pymysql
import traceback
import json
import functools
from database import *
from sql_queries import *
import itertools
app = Flask(__name__)
JSON_SORT_KEYS = False
@app.route('/api/v1.0/cost-explorer', methods=['GET'])
def get_cost_explorer():

    clients = request.args.getlist('clients[]')
    projects = request.args.getlist('projects[]')
    cost_types = request.args.getlist('cost_types[]')

    obj = Manager()
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


class Manager(DataBase):

    """
    This main controller of processing data from database and make result.
    """

    def __init__(self):
        self.connection_details = {

        }
        self.read_db_config('db.config')
        print self.connection_details
        DataBase.__init__(self)

    def read_db_config(self, file_name):
        try:
            f = open(file_name, "r")
            for line in f:
                if line and not line.strip().startswith("#"):
                    key, value = line.split("=")
                    self.connection_details[key.strip()] = value.strip()
            f.close()
        except Exception, msg:
            print "Exception in readMasterConfig", msg, file_name

    def get_details(self, clients, projects, cost_types):
        """
        This actual controller function which accept filter params and do processing. This include first level client
        and project details.
        :param clients:
        :param projects:
        :param cost_types:
        :return parent_json:
        """

        try:

            self.create_connection_obj()
            project_where_condition = ""
            clients_where_condition = ""
            cost_types_where_condition = ""

            if len(projects) > 0:
                project_where_condition = "where ID in (%s)" % ','.join(projects)
            if len(clients) > 0 :
                clients_where_condition = "where ID in (%s)" % ','.join(clients)

            if len(cost_types) > 0:
                cost_types_where_condition = "where ID in (%s)" % ','.join(cost_types)

            sql_get_data = sql_get_clients.replace('{projectCondition}', project_where_condition)
            sql_get_data = sql_get_data.replace('{clientCondition}', clients_where_condition)
            clients_result = self.execute_statement(sql_get_data, parameters=())
            project_cost, client_cost = self.get_project_cost_details(project_where_condition,clients_where_condition,cost_types_where_condition)
            parent_json = []
            i = 0
            for client in clients_result:
                parent_json.append({
                    'id': client.get('ID'),
                    'name': client.get('client'),
                    'amount': client_cost.get(str(client.get('ID')))['amount']
                })
                index = len(parent_json) - 1
                for project in client.get('projectID').split(","):
                    parent_json[index]['breakdown'] = project_cost.get(str(project))

            return parent_json
        except Exception as e:
            exe_stack_trace = traceback.format_exc()
            print "Error while fetching client and project information---", exe_stack_trace

    def get_project_cost_details(self,project_where_condition,clients_where_condition,cost_types_where_condition):

        """
        This function to get cost details project wise and tree structure wise. Result return flat structure data. Then it convert
        nested tree like structure.
        """
        try:
            sql_get_data = sql_get_project_cost.replace('{projectCondition}', project_where_condition)
            sql_get_data = sql_get_data.replace('{clientCondition}', clients_where_condition)
            sql_get_data = sql_get_data.replace('{costTypeCondition}', cost_types_where_condition)
            project_cost_details = self.execute_statement(sql_get_data,parameters=())
            cost_group_list = {}
            project_cost = {}
            client_cost = {}
            i = 0
            for cost in project_cost_details:

                client_id = str(cost.get('Client_ID'))
                project_id = str(cost.get('Project_ID'))
                parent_cost_type_id = str(cost.get('Parent_Cost_Type_ID'))
                if client_id not in client_cost:
                    client_cost[client_id] = {}
                if parent_cost_type_id == '0':
                    if 'amount' not in client_cost[client_id]:
                        client_cost[client_id]['amount'] = 0
                    client_cost[client_id]['amount'] += int(cost.get('Amount'))

                if project_id not in project_cost:
                    project_cost[project_id] = {}
                if "breakdown" not in project_cost[project_id]:
                    project_cost[project_id]["breakdown"] = []
                if 'amount' not in project_cost[project_id]:
                    project_cost[project_id]['amount'] = 0

                project_cost[project_id]['name'] = cost.get('Title')
                project_cost[project_id]['id'] = cost.get('Project_ID')
                if parent_cost_type_id == '0':
                    project_cost[project_id]['amount'] += int(cost.get('Amount'))

                project_cost[project_id]["breakdown"].append(
                    {
                        'amount': int(cost.get('Amount')),
                        'name': cost.get('Name'),
                        'parent_id': parent_cost_type_id,
                        'id' : cost.get('Cost_Type_ID')
                    }
                )

            project_cost_tree = self.get_tree_from_flat(project_cost)

            return project_cost_tree, client_cost

        except Exception as e:
            exe_stack_trace = traceback.format_exc()
            print "Error while fetching cost information by project and types---", exe_stack_trace

    def get_tree_from_flat(self,project_cost):

        """
        This function to create tree or nested parent child releation based on key parameters from
        flat structure. Input expected list of values.
        :param project_cost:
        :return:
        """
        for data in project_cost.values():
            # print data
            project_data = data['breakdown']

            result = {x.get("id"): x for x in project_data}
            # print(result)
            tree = []
            for a in project_data:
                # print(a)
                if int(a.get("parent_id")) in result:
                    parent = result[int(a.get("parent_id"))]
                else:
                    parent = ""
                if parent:
                    if "breakdown" not in parent:
                        parent["breakdown"] = []
                    parent["breakdown"].append(a)

                else:
                    tree.append(a)
        return project_cost

# flask-rest-api
This is REST API developed using python flask framework. To get data from database using GET method. 

## General guidelines for API 

* A URL identifies a resource.
* This REST API only allow GET method ( other method POST, PUT,PATCH, DELETE doesn't work).
* lookup parameter is not mandatory to work. 
* This API will in website or UI to get costing of project by client or cost types

API without parameters : 
http://localhost:5000/api/v1.0/cost-explorer

API with all parameters: 
http://localhost:5000/api/v1.0/cost-explorer?clients[]=2&projects[]=1&cost_types[]=1&cost_types[]=2&cost_types[]=3

## Error handling

Error responses should include a common HTTP status code, message for the developer, message for the end-user (when appropriate), internal error code (corresponding to some specific internally determined ID), links where developers can find more info. For example:

 
Use three simple, common response codes indicating (1) success, (2) failure due to client-side problem, (3) failure due to server-side problem:
* 200 - OK
* 400 - Bad Request
* 500 - Internal Server Error
* 405 - Method not found

### GET /genes

Example: http://example.com/api/v1.0/cost-explorer

Response body:

    [
    {
        "amount": 926471,
        "breakdown": {
            "amount": 442228,
            "breakdown": [
                {
                    "amount": 259428,
                    "id": 1,
                    "name": "Development",
                    "parent_id": "0"
                },
                {
                    "amount": 101824,
                    "id": 2,
                    "name": "Designing",
                    "parent_id": "0"
                },
                {
                    "amount": 80976,
                    "id": 3,
                    "name": "Marketing",
                    "parent_id": "0"
                }
            ],
            "id": 1,
            "name": "Project 1"
        },
        "id": 1,
        "name": "Avengers"
    },
    {
        "amount": 1574544,
        "breakdown": {
            "amount": 529993,
            "breakdown": [
                {
                    "amount": 320469,
                    "id": 1,
                    "name": "Development",
                    "parent_id": "0"
                },
                {
                    "amount": 137880,
                    "id": 2,
                    "name": "Designing",
                    "parent_id": "0"
                },
                {
                    "amount": 71644,
                    "id": 3,
                    "name": "Marketing",
                    "parent_id": "0"
                }
            ],
            "id": 3,
            "name": "Project 3"
        },
        "id": 2,
        "name": "Defenders"
    }]


## Application run guidelines :
* open terminal and go to project run
* run command
    `python run.py`
* `db.config` is symbolic link to `db-local.config` while doing on production have to change to `db-prod.config`

## Postman Request 

https://www.getpostman.com/collections/6a6492a0f0221350d247

## Versions

* V1.0

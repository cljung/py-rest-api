from flask import Flask
from flask import request
from flask import Response
from flask.json import jsonify
import json
import logging
import sys, os, tempfile, uuid, time, datetime
import jwtvalidator
import restapihelper
import configparser
import argparse, sys

app = Flask(__name__)

log = logging.getLogger() #'werkzeug')
log.setLevel(logging.INFO)

tenantId = ""
appId = ""
args = None

itemList = []
itemList.append( {"id" : '001002003', 'Description' : 'First Item'} )
itemList.append( {"id" : '002003004', 'Description' : 'Second Item'} )
itemList.append( {"id" : '003004005', 'Description' : 'Third Item'} )

# https://code.visualstudio.com/docs/python/tutorial-deploy-app-service-on-linux
# https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python
# https://docs.microsoft.com/en-us/azure/app-service/containers/app-service-linux-intro
# http://blog.luisrei.com/articles/flaskrest.html
# https://joonasw.net/view/defining-permissions-and-roles-in-aad

# public api to check connectivity
@app.route("/", methods = ['GET'])
def hello():
    buildTag = ""
    if "BUILDTAG" in os.environ:
       buildTag = "<br/>Build Tag: " + os.environ["BUILDTAG"]
    return "Hello from py-rest-api!<br/>Azure AD TenantID: " + tenantId + "<br/>Azure AD AppID: " + appId + "<br/>" + datetime.datetime.utcnow().isoformat() + buildTag

# api that requires auth and returns info about user
@app.route("/api/echo", methods = ['GET'])
def echoApi():
    jwt_decoded, resp = jwtvalidator.checkAuthorization()
    if resp:
       return resp
    expTime = datetime.datetime.fromtimestamp( jwt_decoded['exp'] ).isoformat()
    return "Hello " + jwt_decoded['upn'] + "! Your access token is valid until " + expTime + "Z"

# api that returns a list of items
@app.route('/api/items', methods = ['GET'])
def listItems():
    jwt_decoded, resp = jwtvalidator.checkAuthorization( "Api.Read" )
    if resp:
       return resp

    resp = Response( json.dumps(itemList), status=200, mimetype='application/json')
    return resp

# api that returns a single item
@app.route('/api/items/<id>', methods = ['GET'])
def getItem(id):
    jwt_decoded, resp = jwtvalidator.checkAuthorization( "Api.Read" )
    if resp:
       return resp

    result=[item for item in itemList if item['id'] == id]
    if len(result) > 0:
       resp = Response( json.dumps(result), status=200, mimetype='application/json')
    else:
       return restapihelper.generateItemNotFoundResponse( id )

    return resp

# api that creates a new item
@app.route('/api/items/<id>', methods = ['POST'])
def createItem(id):
    jwt_decoded, resp = jwtvalidator.checkAuthorization( "Api.Write" )
    if resp:
       return resp

    resp = restapihelper.validateContentType( 'application/json' )
    if resp:
       return resp

    resp = restapihelper.validateRequestBody()
    if resp:
       return resp

    result=[item for item in itemList if item['id'] == id]
    if len(result) > 0:
       return restapihelper.generateItemAlreadyExists( id )

    appData = json.loads( request.data )
    itemList.append( appData )
    return restapihelper.generateItemCreatedResponse( id )

# api that updates an existing item
@app.route('/api/items/<id>', methods = ['PUT', 'PATCH'])
def updateItem(id):
    jwt_decoded, resp = jwtvalidator.checkAuthorization( "Api.Write" )
    if resp:
       return resp

    resp = restapihelper.validateContentType( 'application/json' )
    if resp:
       return resp

    resp = restapihelper.validateRequestBody()
    if resp:
       return resp

    appData = json.loads( request.data )
    for i in range (len(itemList)):
       if itemList[i]['id'] == id:
          itemList[i] = appData
          return restapihelper.generateItemUpdatedResponse( id )

    return restapihelper.generateItemNotFoundResponse( id )

# api that removes an existing item
@app.route('/api/items/<id>', methods = ['DELETE'])
def deleteItem(id):
    jwt_decoded, resp = jwtvalidator.checkAuthorization( "Api.Write" )
    if resp:
       return resp

    for i in range (len(itemList)):
       if itemList[i]['id'] == id:
          del itemList[i]
          return restapihelper.generateItemRemovedResponse( id )

    return restapihelper.generateItemNotFoundResponse( id )

tenantId = os.environ['AZTENANTID']
appId = os.environ['AZAPPID']

jwtvalidator.initAzureAD( tenantId, appId )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

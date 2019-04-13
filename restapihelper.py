from flask import Flask
from flask import request
from flask import Response
from flask.json import jsonify
import json

def validateContentType(validContentType):
    # don't know which ones we should support, but these are the obvious ones
    validContentTypes = ['application/json']
    # if given image data, save it as a temp file
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != validContentTypes:
        msg = {"message" : 'Unsupported Content Type ' + request.headers['Content-Type'] + '. Must be ' + validateContentType}
        return Response( json.dumps(msg), status=415, mimetype='application/json')

    return None

def validateRequestBody():
    # check that caller send data in request body
    if len(request.data) == 0:
        msg = {"message" : 'No data in request body'}
        return Response( json.dumps(msg), status=400, mimetype='application/json')

    return None

def generateItemNotFoundResponse(id):
    msg = {"message" : 'Item not found: ' + id}
    return Response( json.dumps(msg), status=404, mimetype='application/json')

def generateItemCreatedResponse(id):
    msg = {"message" : 'Item created: ' + id}
    return Response( json.dumps(msg), status=201, mimetype='application/json')

def generateItemUpdatedResponse(id):
    msg = {"message" : 'Item updated: ' + id}
    return Response( json.dumps(msg), status=200, mimetype='application/json')

def generateItemRemovedResponse(id):
    msg = {"message" : 'Item removed: ' + id}
    return Response( json.dumps(msg), status=200, mimetype='application/json')

def generateItemAlreadyExists(id):
    msg = {"message" : 'Item already exists: ' + id}
    return Response( json.dumps(msg), status=409, mimetype='application/json')

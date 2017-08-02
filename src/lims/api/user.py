from flask import jsonify
from flask import request
from flask_security import login_required

from sa_jsonapi import serializer as jsonapi
from lims import db, api




@api.route('/user')
def get_users():
    response = jsonapi.get_collection(db.session, request.args, 'users')
    print "hihi"
    return jsonify(response.document), response.status



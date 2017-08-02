from flask import Blueprint
from lims import app


api = Blueprint('api', app.import_name, url_prefix='/api')


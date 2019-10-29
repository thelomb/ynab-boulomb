from flask import Blueprint

bp = Blueprint('reports', __name__)

from application.reports import routes

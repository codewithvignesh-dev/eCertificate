from flask import Blueprint

certificates = Blueprint("certificates", __name__)

from . import routes
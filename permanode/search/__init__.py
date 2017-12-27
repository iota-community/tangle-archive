from flask import Blueprint


search = Blueprint('search', __name__)

from permanode.search import api  # NOQA

from flask import Blueprint


bundles = Blueprint('bundles', __name__)

from permanode.bundles import api  # NOQA

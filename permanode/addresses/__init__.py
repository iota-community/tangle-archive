from flask import Blueprint


addresses = Blueprint('addresses', __name__)

from permanode.addresses import api  # NOQA

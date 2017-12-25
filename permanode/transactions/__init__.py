from flask import Blueprint


transactions = Blueprint('transactions', __name__)

from permanode.transactions import api  # NOQA

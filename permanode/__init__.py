from flask import Flask
from config import config
from flask_cqlalchemy import CQLAlchemy

db = CQLAlchemy()


def init(configuration):
    app = Flask(__name__)
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)

    db.init_app(app)

    from permanode.search import search as search_blueprint

    app.register_blueprint(search_blueprint, url_prefix='/api/v1')

    return app

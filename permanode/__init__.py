from flask import Flask
from config import config
from flask_cqlalchemy import CQLAlchemy

db = CQLAlchemy()


def init(configuration):
    app = Flask(__name__)
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)

    db.init_app(app)

    from permanode.addresses import addresses as addresses_blueprint
    from permanode.transactions import transactions as transactions_blueprint
    from permanode.bundles import bundles as bundles_blueprint
    from permanode.search import search as search_blueprint

    app.register_blueprint(addresses_blueprint)
    app.register_blueprint(transactions_blueprint)
    app.register_blueprint(bundles_blueprint)
    app.register_blueprint(search_blueprint, url_prefix='/api/v1')

    return app

from flask import Flask
from config import config


def init(configuration):
    app = Flask(__name__)
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)

    from permanode.addresses import addresses as addresses_blueprint

    app.register_blueprint(addresses_blueprint)

    return app

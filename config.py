import ssl


class BaseConfig:
    """
    cassandra configuration
    """

    CASSANDRA_HOSTS = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'cqlengine'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    port = 8080


class ProductionConfig(BaseConfig):
    ssl_options = {
                      'ca_certs': './certs/rootCa.crt',
                      'ssl_version': ssl.PROTOCOL_TLSv1
                  }
    # Setting cassandra args for ssl_options
    CASSANDRA_SETUP_KWARGS = {
        'ssl_options': ssl_options
    }


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

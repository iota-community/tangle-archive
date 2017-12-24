class BaseConfig:
    """
    cassandra configuration
    """

    CASSANDRA_HOSTS = ['13.90.99.22']
    CASSANDRA_KEYSPACE = 'cqlengine'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    port = 8080


config = {
    'development': DevelopmentConfig
}

import ssl

class BaseConfig:
    """
    cassandra configuration
    """

    # ssl_options = {
    #                   'ca_certs': './certs/rootCa.crt',
    #                   'ssl_version': ssl.PROTOCOL_TLSv1
    #               }

    CASSANDRA_HOSTS = ['cassandra']
    CASSANDRA_KEYSPACE = 'cqlengine'
    # CASSANDRA_SETUP_KWARGS = {
    #     'ssl_options' : ssl_options
    # }
   
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    port = 8080


config = {
    'development': DevelopmentConfig
}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LEVELUP_MAIL_SUBJECT_PREFIX = '[LevelUP] '
    LEVELUP_MAIL_SENDER = 'LevelUP Admin <rkhillah.developer@gmail.com>'
    LEVELUP_ADMIN = os.environ.get('LEVELUP_ADMIN') or ['rkhillah.developer@gmail.com']
    LEVELUP_POSTS_PER_PAGE = os.environ.get('LEVELUP_POSTS_PER_PAGE') or 20
    LEVELUP_FOLLOWERS_PER_PAGE = os.environ.get('LEVELUP_FOLLOWERS_PER_PAGE') or 50
    LEVELUP_COMMENTS_PER_PAGE = os.environ.get('LEVELUP_COMMENTS_PER_PAGE') or 30
    LEVELUP_SLOW_DB_QUERY_TIME = 0.5
    SSL_REDIRECT = False

    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_BINDS = {
        'township_data': os.environ.get('DEV_TOWNSHIP_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'township-data-dev.sqlite'),
        'user_data': os.environ.get('DEV_USERS_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'users-data-dev.sqlite'),
    }

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_BINDS = {
        'township_data': os.environ.get('TOWNSHIP_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'township-data.sqlite'),
        'user_data': os.environ.get('USERS_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'users-data.sqlite'),
    }
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None) is not None:
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.LEVELUP_MAIL_SENDER,
            toaddrs=[cls.LEVELUP_ADMIN],
            subject=cls.LEVELUP_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    SQLALCHEMY_BINDS = {
        'township_data': os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'township-data.sqlite'),
        'user_data': os.environ.get('HEROKU_POSTGRESQL_AMBER_URL') or \
            'sqlite:///' + os.path.join(basedir, 'users-data.sqlite'),
    }

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class HerokuConfigStaging(HerokuConfig):
    SQLALCHEMY_BINDS = {
        'township_data': os.environ.get('DATABASE_URL') or \
            os.environ.get('DEV_TOWNSHIP_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'township-data.sqlite'),
        'user_data': os.environ.get('HEROKU_POSTGRESQL_BLUE_URL') or \
            os.environ.get('DEV_USERS_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'users-data.sqlite'),
    }

    @classmethod
    def init_app(cls, app):
        HerokuConfig.init_app(app)

# Register configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'heroku_staging': HerokuConfigStaging,

    'default': DevelopmentConfig
}

import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'APP_SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ["S3_BUCKET"]
    S3_KEY = os.environ["S3_KEY"]
    S3_SECRET = os.environ["S3_SECRET_ACCESS_KEY"]
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    FLIGHT_API_KEY = os.environ["FLIGHT_API_KEY"]

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True

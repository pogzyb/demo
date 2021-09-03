import os


class Config:
    VERSION = os.getenv('VERSION')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


def get_app_config(env: str):
    configs = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig',
    }
    return configs.get(env, 'config.DevelopmentConfig')
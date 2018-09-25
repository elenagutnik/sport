# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SCOREBOARD_HOST = '127.0.0.1'
    SCOREBOARD_PORT = 7001
    LANGUAGES = {
        'en': 'English',
        'ru': 'Русский'
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:123123@localhost:5432/sport'

    SQLALCHEMY_BINDS = {'shorttrack': 'postgresql://postgres:123123@localhost:5432/shorttrack'}


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://postgres:123123@localhost:5432/sport'
    SQLALCHEMY_BINDS = {'shorttrack': 'postgresql://postgres:123123@localhost:5432/shorttrack'}


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123123@localhost:5432/sport'
    SQLALCHEMY_BINDS = {'shorttrack': 'postgresql://postgres:123123@localhost:5432/shorttrack'}


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

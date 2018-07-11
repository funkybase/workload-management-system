import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://kebfrihb:as-iqLWJZ7ygeKnLsPEwRDA3BAectUVQ@stampy.db.elephantsql.com:5432/kebfrihb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

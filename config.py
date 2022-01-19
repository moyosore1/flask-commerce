import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "mysecret123"
    SQLALCHEMY_DATABASE_URI ="postgresql://qwyrajamzlowqe:8ca1f1957ff6b5c17d61d27c670c53da6dc7adb4d527a735f31e88a29635f6ad@ec2-3-95-118-1.compute-1.amazonaws.com:5432/dd2vi3ul81m9nf"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
    pass

class Development(Config):
    DEBUG = True
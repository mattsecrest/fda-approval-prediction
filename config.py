import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e256803842b0ac38c491bc4ff193e809587b1ef2b6915b9cd746b46b8978883a'
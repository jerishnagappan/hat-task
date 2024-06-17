import os
import configparser

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def load_config():
    config = configparser.ConfigParser()
    config.read('confi.ini')
    return config['DATABASE']['SQLALCHEMY_DATABASE_URI']

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = load_config()
    
    return app    

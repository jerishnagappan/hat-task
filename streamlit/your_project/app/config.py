import configparser

config = configparser.ConfigParser()
config.read('/Users/jerish.nagappan/Documents/streamlit/your_project/confi.ini')
SQLALCHEMY_DATABASE_URI = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
    

SQLALCHEMY_TRACK_MODIFICATIONS = False












# import os
# import configparser
# from flask import Flask

# class Config:
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# def load_config():
#     config = configparser.ConfigParser()
#     config.read('confi.ini')
#     return config['DATABASE']['SQLALCHEMY_DATABASE_URI']

# def create_app():
#     app = Flask(__name__)
    
#     app.config.from_object(Config)
#     app.config['SQLALCHEMY_DATABASE_URI'] = load_config()
    
#     return app

# config.py

# SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
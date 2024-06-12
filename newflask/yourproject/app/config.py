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


# import configparser

# config = configparser.ConfigParser()
# config.read('confi.ini')

# class Config:
#     DEBUG = False
#     TESTING = False
#     SQLALCHEMY_DATABASE_URI = config['DATABASE']['SQLALCHEMY_DATABASE_URI']
#     # Add other configuration variables as needed



# import os
# import configparser

# config_path = '/Users/jerish.nagappan/Documents/newflask/yourproject/confi.ini'
# config = configparser.ConfigParser()
# config.read(config_path)

# print("Current working directory:", os.getcwd())


# import os
# import configparser

# class Config:
#     def __init__(self, config_path):
#         self.config = configparser.ConfigParser()
#         self.config_path = config_path
#         self.read_config()

#     def read_config(self):
#         if not os.path.exists(self.config_path):
#             raise FileNotFoundError(f"Config file '{self.config_path}' not found.")
#         self.config.read(self.config_path)

#     def get_config_value(self, section, key):
#         return self.config.get(section, key)

    
# config_path = '/Users/jerish.nagappan/Documents/newflask/yourproject/confi.ini'
# app_config = Config(config_path)


# database_uri = app_config.get_config_value('DATABASE', 'SQLALCHEMY_DATABASE_URI')



# import configparser

# def load_config():
#     config = configparser.ConfigParser()
#     config.read('confi.ini')
#     return config['DATABASE']['SQLALCHEMY_DATABASE_URI']


# from flask import Flask
# from app.config import load_config

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = load_config()

#     # Other app setup...

#     return app



# class AppConfig:
#     def __init__(self):
#         self.config = configparser.ConfigParser()
#         self.config_path = 'confi.ini'
#         self.read_config()

#     def read_config(self):
#         self.config.read(self.config_path)

#     def get_database_uri(self):
#         return self.config['DATABASE']['SQLALCHEMY_DATABASE_URI']


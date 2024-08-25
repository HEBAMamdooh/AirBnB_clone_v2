#!/usr/bin/python3
"""create a unique FileStorage or DbStorage instance for your application"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import environ

sqlStorage = environ.get('HBNB_TYPE_STORAGE')

if sqlStorage == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()

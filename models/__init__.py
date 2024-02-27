#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ
from models.engine import file_storage, db_storage

if 'HBNB_TYPE_STORAGE' in environ and environ['HBNB_TYPE_STORAGE'] == 'db':
    storage = db_storage.DBStorage()
else:
    storage = file_storage.FileStorage()

storage.reload()

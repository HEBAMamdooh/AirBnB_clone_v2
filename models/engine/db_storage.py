#!/usr/bin/python3
"""This is the file storage class for AirBnB"""

from os import environ
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """To Represents a database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Query objects in the session."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(environ['HBNB_MYSQL_USER'],
                                              environ['HBNB_MYSQL_PWD'],
                                              environ['HBNB_MYSQL_HOST'],
                                              environ['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session
        all objects depending of the class name (argument object)
        """

        session = self.__session
        object = {}
        if not cls:
            tables = [User, State, City, Amenity, Place, Review]

        else:
            if type(cls) == str:
                cls = eval(cls)

            tables = [cls]

        for t in tables:
            query = session.query(t).all()

            for rows in query:
                key = "{}.{}".format(type(rows).__name__, rows.id)
                object[key] = rows

        return object

    def new(self, obj):
        """new obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """save all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

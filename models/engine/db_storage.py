from os import environ
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """To Represents a database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Query objects in the session. Returns <class name>.<obj id> = obj dict."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(environ['HBNB_MYSQL_USER'],
                                              environ['HBNB_MYSQL_PWD'],
                                              environ['HBNB_MYSQL_HOST'],
                                              environ['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        classes = ["State", "City"]  # Add other classes as needed
        objs = {}
        if cls:
            classes = [cls.__name__]
        for c in classes:
            for obj in self.__session.query(eval(c)).all():
                objs[obj.__class__.__name__ + '.' + obj.id] = obj
        return objs

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
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

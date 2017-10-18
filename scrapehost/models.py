import time
import datetime
import json


class DBObject(object):
    """This class defines how objects in the mongoDB should be represented."""

    def __init__(
            self,
            classes=[],
            type='',
            meta={}
            ):
        self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        self.classes = classes
        self.type = type
        self.meta = meta
        self.structure = '{}{}'.format('#', self.__class__.__name__)

    def export(self):
        """This function exports the object as a dict. This is used when
        putting an object in the database."""

        return self.__dict__

class User(DBObject):
    def __init__(
            self,
            email=None,
            password=None,
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.email = email
        self.password = password

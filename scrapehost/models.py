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
            accepted_agreement=False,
            agreement_content=None, # the accepted agreement
            token=None,
            forgot_password_token=None,
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.email = email
        self.password = password
        self.accepted_agreement = accepted_agreement
        self.agreement_content = agreement_content
        self.token = token
        self.forgot_password_token = forgot_password_token

class Scraper(DBObject):
    def __init__(
            self,
            name=None,
            location=None, # user input
            url_index=0,
            visited_urls=[],
            found_urls=[],
            user_id=None,
            status=1,
            query=None,
            data=[],
            domain_restrict=False,
            plan=1, # 0 = basic, 1 = standard, 2 = pro
            error=None,
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.name = name
        self.location = location
        self.url_index = url_index
        self.visited_urls = visited_urls
        self.found_urls = found_urls
        self.user_id = user_id
        self.status = status
        self.query = query
        self.data = data
        self.domain_restrict = domain_restrict
        self.plan = plan
        self.error = error

class Order(DBObject):
    def __init__(
            self,
            object=None,
            object_id=None,
            done=False,
            user_id=None,
            canceled=False,
            price=None,
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.object = object
        self.object_id = object_id
        self.done = done
        self.user_id = user_id
        self.canceled = canceled
        self.price = price

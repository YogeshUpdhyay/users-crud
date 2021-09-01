from mongoengine import Document
from mongoengine.fields import *

class Users(Document):
    user_id = IntField(unique=True)
    first_name = StringField()
    last_name = StringField()
    company_name = StringField()
    city = StringField()
    state = StringField()
    zip = IntField()
    email = EmailField()
    web = URLField()
    age = IntField()

    meta = {'indexes': [
        {'fields': ['$first_name', "$last_name"],
         'default_language': 'english',
        }
    ]}

    def payload(self):
        return {
            "id" : self.user_id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "company_name" : self.company_name,
            "city" : self.city,
            "state" : self.state,
            "zip" : self.zip,
            "email" : self.email,
            "web" : self.web,
            "age" : self.age
        }

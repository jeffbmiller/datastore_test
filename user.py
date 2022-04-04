from google.cloud import ndb

class User(ndb.Model):
    uid = ndb.StringProperty()
    email = ndb.StringProperty()
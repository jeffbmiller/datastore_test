from google.cloud import ndb

class Movie(ndb.Model):
    name = ndb.StringProperty()
    release_date = ndb.DateProperty()
    stars = ndb.IntegerProperty()
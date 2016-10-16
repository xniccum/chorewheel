from google.appengine.ext import ndb


class Kid(ndb.Model):
    name = ndb.StringProperty()
    month = ndb.StringProperty()
    day = ndb.StringProperty()
    year = ndb.StringProperty()
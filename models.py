from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty()
    groups = ndb.KeyProperty(kind='Group', repeated=True)
    
class Group(ndb.Model):
    admins = ndb.KeyProperty(kind='User', repeated=True)
    members = ndb.KeyProperty(kind='User', repeated=True)
    name = ndb.StringProperty()

class Chore(ndb.Model):
    name = ndb.StringProperty()
    due = ndb.DateTimeProperty()
    frequency = ndb.StringProperty()
    points = ndb.IntegerProperty()
    readyForApproval = ndb.BooleanProperty()
    group_id = ndb.KeyProperty(kind='Group')
    assigned_to = ndb.KeyProperty(kind='User')
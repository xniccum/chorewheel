from google.appengine.ext import ndb
from google.appengine.ext import db


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    groups = ndb.KeyProperty(kind='Group', repeated=True)

    PARENT_KEY = ndb.Key("User", "root")

    @classmethod
    def get_by_user(cls, user):
        return cls.query(ancestor=User.PARENT_KEY).filter(cls.email == user.email().lower()).get()

    @classmethod
    def get_groups(cls, google_user):
        member = cls.query(ancestor=cls.PARENT_KEY).filter(cls.email == google_user.email().lower()).get()
        groups = []
        for group in member.groups:
            groups.append(group.get())
        return groups


class Group(ndb.Model):
    admins = ndb.KeyProperty(kind='User', repeated=True)
    members = ndb.KeyProperty(kind='User', repeated=True)
    name = ndb.StringProperty()

    PARENT_KEY = ndb.Key("Group", "root")

    @classmethod
    def get_members_from_key(cls, key):
        members = []
        for member in key.get().members:
            members.append(member.get())
        return members

    @classmethod
    def insert_group(cls, user, name):
        group = Group(parent=cls.PARENT_KEY,
                      name=name,
                      admins=[user.key],
                      members=[user.key])
        key = group.put()
        user.groups.append(key)
        user.put()

    @classmethod
    def delete_group(cls, key):
        users_query = User.query(ancestor=User.PARENT_KEY)
        for u in users_query:
            i = 0
            changed = False
            for g in u.groups:
                if str(key) == str(u.groups[i]):
                    del u.groups[i]
                    changed = True
                i += 1
            if changed:
                u.put()
        key.delete()


class Chore(ndb.Model):
    name = ndb.StringProperty()
    due = ndb.DateTimeProperty()
    frequency = ndb.StringProperty()
    points = ndb.IntegerProperty()
    readyForApproval = ndb.BooleanProperty()
    group_id = ndb.KeyProperty(kind='Group')
    assigned_to = ndb.KeyProperty(kind='User')

    PARENT_KEY = ndb.Key("Chore", "root")

    @classmethod
    def get_by_group(cls, group_id):
        return cls.query(ancestor=cls.PARENT_KEY).filter(cls.group_id == group_id)
    
    @classmethod
    def get_upcoming_by_user(cls, user_id):
        return cls.query(ancestor=cls.PARENT_KEY).filter(cls.assigned_to == user_id, cls.readyForApproval == False).order(cls.due)
    

from handlers import base_handlers
from google.appengine.ext import ndb
from models import User


class InsertMember(base_handlers.BaseAction):
    def handle_post(self, google_user):
        group_key = ndb.Key(urlsafe=self.request.get("group-key"))
        group = group_key.get()
        if self.request.get("member-key"):
            pass
            member_key = ndb.Key(urlsafe=self.request.get("member-key"))
            member = member_key.get()
        else:
            member = User.query(ancestor=User.PARENT_KEY).filter(User.email == self.request.get("member-email")).get()
            if not member:
                member = User(parent=User.PARENT_KEY,
                              email=self.request.get("member-email"),
                              groups=[group_key])
            key = member.put()
            if self.request.get("member-admin"):
                group.admins.append(key)
            group.members.append(key)
            group.put()
        self.redirect(self.request.referer)


class DeleteMember(base_handlers.BaseAction):
    def handle_post(self, user):
        # Delete member from group
        member_key = ndb.Key(urlsafe=self.request.get('member-key'))
        group_key = self.request.get("group-key")
        group = group_key.get()
        group.members.remove(member_key)
        group.admins.remove(member_key)
        group.put()
        self.redirect(self.request.referer)
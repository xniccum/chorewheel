from google.appengine.api import app_identity
from google.appengine.api import mail

from handlers import base_handlers
from google.appengine.ext import ndb
from models import User


class InsertMember(base_handlers.BaseAction):
    def handle_post(self, google_user):
        group_key = ndb.Key(urlsafe=self.request.get("group-key"))
        group = group_key.get()
        if self.request.get("send"):
            email = self.request.get("member-email")
            if mail.is_email_valid(email):
                url = "http://chore-wheel-project.appspot.com/invite?"
                url += "group-key="+self.request.get("group-key")+"&"
                url += "email="+self.request.get("member-email")+"&"
                url += "admin="+self.request.get("member-admin")

                sender_address = ('Chore-Wheel.com Support <{}@appspot.gserviceaccount.com>'.format(app_identity.get_application_id()))
                subject = "Chore-Wheel Invitation"
                body="""You have been invited to join the {} Chore-Wheel group
                If you wish to join this group, go to:

                {}""".format(group.name, url)
                mail.send_mail(sender_address, email, subject, body)
            else:
                pass
        elif self.request.get("member-key"):
            member_key = ndb.Key(urlsafe=self.request.get("member-key"))
            if bool(self.request.get("member-admin")):
                group.admins.append(member_key)
            else:
                group.admins.remove(member_key)
            group.put()
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
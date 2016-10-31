from handlers import base_handlers
import main
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Group, User, Chore


class MemberPage(webapp2.RequestHandler):
    def get(self):
        google_user = users.get_current_user()
        if not google_user:
            raise Exception("Missing user!")
        group_key = ndb.Key(urlsafe=self.request.get("groupkey"))
        members = []
        points = {}
        for member_key in group_key.get().members:
            member = member_key.get()
            members.append(member)
            # chores = Chore.query(ancestor=Chore.PARENT_KEY).filter(Chore.assigned_to == member_key)
            # if chores.count() != 0:
            #     sum = 0
            #     for chore in chores:
            #         sum += chore.points
            # points[member] = points
        values = {"user_email": google_user.email().lower(),
                  "logout_url": users.create_logout_url("/"),
                  "members": members,
                  #"points": points,
                  "groupkey": group_key}
        template = main.jinja_env.get_template("templates/members.html")
        self.response.out.write(template.render(values))


class InsertMember(base_handlers.BaseAction):
    def handle_post(self, google_user):
        group_key = ndb.Key(urlsafe=self.request.get("groupkey"))
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
        #Delete member from group
        member_key = ndb.Key(urlsafe=self.request.get('member-key'))
        group_key = self.request.get("groupkey")
        group = group_key.get()
        group.members.remove(member_key)
        group.admins.remove(member_key)
        group.put()
        self.redirect(self.request.referer)
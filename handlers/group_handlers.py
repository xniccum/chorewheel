from handlers import base_handlers
from google.appengine.ext import ndb
from models import Group,User


class GroupPage(base_handlers.BasePage):
    def get_template(self):
        return "templates/groups.html"

    def update_values(self, user, values):
        member = User.query(User.email == user.email()).get()
        groups = []
        for group in member.groups:
            groups.append(group.get())
        values["groups"] = groups


class InsertGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        member = User.query(User.email == user.email()).get()
        if self.request.get("group-key"):
            group_key = ndb.Key(urlsafe=self.request.get("group-key"))
            group = group_key.get()
            group.name = self.request.get("name")
        else:
            group = Group(name=self.request.get("name"),
                          admins=[member.key.urlsafe()],
                          members=[member.key.urlsafe()])

        group.put()
        self.redirect(self.request.referer)


class DeleteGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        group_key = ndb.Key(urlsafe=self.request.get('key'))
        group_key.delete()
        self.redirect(self.request.referer)

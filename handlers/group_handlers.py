from handlers import base_handlers
from google.appengine.ext import ndb
from models import Group,User


class GroupPage(base_handlers.BasePage):
    def get_template(self):
        return "templates/groups.html"

    def update_values(self, user, values):
        values["groups"] = User.query(User.email == user.email())


class InsertGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        if self.request.get("key"):
            group_key = ndb.Key(urlsafe=self.request.get("key"))
            group = group_key.get()
            group.name = self.request.get("name")
        else:
            group = Group(name=self.request.get("name"))

        group.put()
        self.redirect("/groups")


class DeleteGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        group_key = ndb.Key(urlsafe=self.request.get('key'))
        group_key.delete()
        self.redirect(self.request.referer)

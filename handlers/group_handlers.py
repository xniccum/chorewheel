from google.appengine.ext import ndb

from handlers import base_handlers
from models import Group, User


class GroupPage(base_handlers.BasePage):
    def get_template(self):
        return "templates/groups.html"

    def update_values(self, google_user, values):
        values["groups"] = User.get_groups(google_user)


class InsertGroup(base_handlers.BaseAction):
    def handle_post(self, google_user):
        if self.request.get("group-key"):
            group_key = ndb.Key(urlsafe=self.request.get("group-key"))
            group = group_key.get()
            group.name = self.request.get("name")
            group.put()
        else:
            user = User.get_by_user(google_user)
            Group.insert_group(user=user,
                               name=self.request.get("name"))
        self.redirect(self.request.referer)


class DeleteGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        group_key = ndb.Key(urlsafe=self.request.get('group-key'))
        Group.delete_group(group_key)
        self.redirect(self.request.referer)

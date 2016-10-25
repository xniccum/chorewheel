import logging

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Group, User


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
            group.put()
        else:
            datastoreUser = User.query(User.email == user.email()).get()
            group = Group(name=self.request.get("name"),
                          admins=[member.key],
                          members=[member.key])
            group.put()
            datastoreUser.groups.append(group.key)
            datastoreUser.put()

        self.redirect(self.request.referer)


class DeleteGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        groupKey = self.request.get('group-key')
        group_key = ndb.Key(urlsafe=groupKey)
        usersQuery = User.query()
        for u in usersQuery:
            i = 0
            for g in u.groups:
                if str(group_key) == str(u.groups[i]):
                    del u.groups[i]
                    u.put()
                i += 1
        group_key.delete()
        self.redirect(self.request.referer)

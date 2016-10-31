from google.appengine.ext import ndb

from handlers import base_handlers
from models import Group, User, Chore


class GroupPage(base_handlers.BasePage):
    def get_template(self):
        if self.request.get("group-key"):
            return "templates/group_detail.html"
        else:
            return "templates/groups.html"

    def update_values(self, google_user, values):
        if self.request.get("group-key"):
            group_key = ndb.Key(urlsafe=self.request.get('group-key'))
            values["groupkey"] = group_key
            values["chores"] = Chore.get_by_group(group_key)
            values["user_key"] = User.get_by_user(google_user)

            members = []
            points = {}
            for member_key in group_key.get().members:
                member = member_key.get()
                members.append(member)
                chores = Chore.query(ancestor=Chore.PARENT_KEY).filter(Chore.assigned_to == member_key)
                sum = 0
                if chores.count() != 0:
                    for chore in chores:
                        sum += chore.points
                points[member.email] = sum

            values["members"] = members
            values["points"] = points
        else:
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

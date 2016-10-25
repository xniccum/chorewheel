from handlers import base_handlers
from google.appengine.ext import ndb
from models import Chore, User


class GroupPage(base_handlers.BasePage):
    def get_template(self):
        return "templates/chores.html"

    def update_values(self, user, values):
        values["chores"] = Chore.query(User.email == user.email()).run()
        values["groupkey"] =


class InsertChore(base_handlers.BaseAction):
    def handle_post(self, user):
        if self.request.get("chore-key"):
            chore_key = ndb.Key(urlsafe=self.request.get("chore-key"))
            chore = chore_key.get()
            chore.name = self.request.get("name")
            chore.due = self.request.get("due")
            chore.frequency = self.request.get("frequency")
            chore.points = self.request.get("points")
        else:
            chore = Chore(name=self.request.get("name"),
                          due=self.request.get("due"),
                          frequency= self.request.get("frequency"),
                          points=self.request.get("points"))

        chore.put()
        self.redirect(self.request.referer)


class DeleteGroup(base_handlers.BaseAction):
    def handle_post(self, user):
        group_key = ndb.Key(urlsafe=self.request.get('chore-key'))
        group_key.delete()
        self.redirect(self.request.referer)
from handlers import base_handlers
import main
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Chore, User


class ChorePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            raise Exception("Missing user!")
        member = User.query(User.email == user.email()).get()
        groupKey = self.request.get('groupkey')
        group_key = ndb.Key(urlsafe=groupKey)
        values = {"user_email": user.email().lower(),
                  "logout_url": users.create_logout_url("/"),
                  "chores": Chore.query(Chore.group_id == group_key),
                  "groupkey": group_key,
                  "user_key": member}
        template = main.jinja_env.get_template("templates/chores.html")
        self.response.out.write(template.render(values))


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


class DeleteChore(base_handlers.BaseAction):
    def handle_post(self, user):
        chore_key = ndb.Key(urlsafe=self.request.get('chore-key'))
        chore_key.delete()
        self.redirect(self.request.referer)
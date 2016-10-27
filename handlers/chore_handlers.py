from handlers import base_handlers
import main
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Chore, User
from utils import date_utils


class ChorePage(webapp2.RequestHandler):
    def get(self):
        google_user = users.get_current_user()
        if not google_user:
            raise Exception("Missing user!")

        group_key = ndb.Key(urlsafe=self.request.get('groupkey'))
        values = {"user_email": google_user.email().lower(),
                  "logout_url": users.create_logout_url("/"),
                  "chores": Chore.get_by_group(group_key),
                  "groupkey": group_key,
                  "user_key": User.get_by_user(google_user)}
        template = main.jinja_env.get_template("templates/chores.html")
        self.response.out.write(template.render(values))
        
class InsertChorePage(base_handlers.BasePage):
    def get_template(self):
        return "templates/insertChore.html"
    
    def update_values(self, user, values):
        if self.request.get("chorekey"):
            chore_key = ndb.Key(urlsafe=self.request.get("chorekey"))
            chore = chore_key.get()
            values["name"] = chore.name
            values["due"] = date_utils.date_time_input_format(chore.due, "US/Eastern")
            values["frequency"] = chore.frequency
            values["points"] = chore.points
            values["groupkey"] = chore.group_id.urlsafe()
            values["chorekey"] = self.request.get("chorekey")
        elif self.request.get("groupkey"):
            values["groupkey"] = self.request.get("groupkey")
        else:
            raise Exception("Incorrect URL parameters passes")


class InsertChore(base_handlers.BaseAction):
    def handle_post(self, google_user):
        if self.request.get("chore-key"):
            chore_key = ndb.Key(urlsafe=self.request.get("chore-key"))
            chore = chore_key.get()
            chore.name = self.request.get("name")
            chore.due = date_utils.get_utc_datetime_from_user_input("US/Eastern", self.request.get("due"))
            chore.frequency = self.request.get("frequency")
            chore.points = int(self.request.get("points"))
        else:
            group_key = ndb.Key(urlsafe=self.request.get("group-key"))
            chore = Chore(parent=Chore.PARENT_KEY,
                          name=self.request.get("name"),
                          due=date_utils.get_utc_datetime_from_user_input("US/Eastern", self.request.get("due")),
                          frequency= self.request.get("frequency"),
                          points=int(self.request.get("points")))
            chore.group_id = group_key.get().key

        chore.put()
        self.redirect("/chores?groupkey=" + self.request.get("group-key"))


class DeleteChore(base_handlers.BaseAction):
    def handle_post(self, user):
        chore_key = ndb.Key(urlsafe=self.request.get('chore-key'))
        chore_key.delete()
        self.redirect(self.request.referer)
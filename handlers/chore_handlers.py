from handlers import base_handlers
from google.appengine.ext import ndb
from models import Chore
from utils import date_utils
from datetime import datetime, timedelta

        
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
                          readyForApproval=False,
                          due=date_utils.get_utc_datetime_from_user_input("US/Eastern", self.request.get("due")),
                          frequency= self.request.get("frequency"),
                          points=int(self.request.get("points")))
            chore.group_id = group_key.get().key

        chore.put()
        self.redirect("/groups?group-key=" + self.request.get("group-key"))


class DeleteChore(base_handlers.BaseAction):
    def handle_post(self, user):
        chore_key = ndb.Key(urlsafe=self.request.get('chore-key'))
        chore_key.delete()
        self.redirect(self.request.referer)
        
class AssignChore(base_handlers.BaseAction):
    def handle_post(self, user):
        assign_to = ndb.Key(urlsafe=self.request.get('assignto'))
        chore_key = ndb.Key(urlsafe=self.request.get('chorekey'))
        chore = chore_key.get()
        chore.assigned_to = assign_to
        chore.readyForApproval = False
        chore.put()

class UnassignChore(base_handlers.BaseAction):
    def handle_post(self, user):
        chore_key = ndb.Key(urlsafe=self.request.get('chorekey'))
        chore = chore_key.get()
        chore.assigned_to = None
        chore.readyForApproval = False
        chore.put()

class MarkChore(base_handlers.BaseAction):
    def handle_post(self, user):
        chore_key = ndb.Key(urlsafe=self.request.get("chorekey"))
        chore = chore_key.get()
        db_user = chore.assigned_to.get()
        if not chore.readyForApproval and db_user.email.lower() == user.email().lower():
            chore.readyForApproval = True
        elif chore.readyForApproval and db_user.email.lower() != user.email().lower():
            chore.readyForApproval = False
            chore.assigned_to = None
            curr_due = datetime.strptime(chore.due, "%m/%d/%y")
            if chore.frequency == "1 day":
                next_due = curr_due + timedelta(days=1)
            elif chore.frequency == "1 week":
                next_due = curr_due + timedelta(days=7)
            elif chore.frequency == "2 week":
                next_due = curr_due + timedelta(days=14)
            elif chore.frequency == "1 month":
                next_due = curr_due + timedelta(days=30)
        else:
            raise Exception("Cannot mark this chore")
        chore.put()
            
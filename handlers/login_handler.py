from handlers import base_handlers
from models import User


class HandleLogin(base_handlers.BaseAction):
    def handle_post(self, google_user):
        user = User.query(ancestor=User.PARENT_KEY).filter(User.email == google_user.email().lower()).get()
        if not user:
            newUser = User(parent=User.PARENT_KEY,
                           name=google_user.nickname(),
                           email=google_user.email().lower(),
                           groups=[])
            newUser.put()
            self.redirect("/groups") 
        elif self.request.get("group-key"):
            user.name = google_user.nickname()
            user.put()
            self.redirect('/groups?group-key='+self.request.get("group-key"))
        else:
            self.redirect("/groups")     
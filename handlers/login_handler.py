from handlers import base_handlers
from models import User


class HandleLogin(base_handlers.BaseAction):
    def handle_post(self, google_user):
        user = User.query(ancestor=User.PARENT_KEY).filter(User.email == google_user.email())
        if user.count() == 0:
            newUser = User(parent=User.PARENT_KEY,
                           email=google_user.email(),
                           groups=[])
            newUser.put()
        self.redirect("/groups")        
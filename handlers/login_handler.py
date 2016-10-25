from handlers import base_handlers
from models import User


class HandleLogin(base_handlers.BaseAction):
    def handle_post(self, user):
        userInDatastore = User.query(User.email == user.email())
        if userInDatastore.count() == 0:
            newUser = User(email = user.email())
            newUser.put()
        self.redirect("/groups")        
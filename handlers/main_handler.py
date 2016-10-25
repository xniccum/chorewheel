from google.appengine.api import users
import webapp2

import main


class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = {}
        values["login_url"] = users.create_login_url("/login-success");
        template = main.jinja_env.get_template("templates/login.html")
        self.response.out.write(template.render(values))
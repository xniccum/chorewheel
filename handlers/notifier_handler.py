import webapp2
from datetime import datetime

from google.appengine.api import app_identity
from google.appengine.api import mail

from models import Chore


class Notify(webapp2.RequestHandler):
    def post(self):
        chores = Chore.query(ancestor=Chore.PARENT_KEY)
        for chore in chores:
            now = datetime.now()
            if chore.due >= now:
                sender_address = 'anything@{}.appspotmail.com'.format(app_identity.get_application_id())
                subject = "Chore-Wheel Invitation"
                email = chore.assigned_to.get().email
                body = """As a reminder, please perform the chore: {}
                Also Remember to check it off and to get it approved""".format(chore.name)
                mail.send_mail(sender_address, email, subject, body)
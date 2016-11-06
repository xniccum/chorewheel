#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import jinja2
import webapp2

from handlers import main_handler, group_handlers, login_handler, chore_handlers, user_handlers


# Jinja environment instance necessary to use Jinja templates.
def __init_jinja_env():
    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
        autoescape=True)
    return jenv

jinja_env = __init_jinja_env()

app = webapp2.WSGIApplication([
    ('/', main_handler.MainHandler),
    
    # Login
    ('/login-success', login_handler.HandleLogin),

    # Group
    ('/groups', group_handlers.GroupPage),

    # Group-CRUD
    ('/add-group', group_handlers.InsertGroup),
    ('/edit-group', group_handlers.InsertGroup),
    ('/delete-group', group_handlers.DeleteGroup),

    # Chores-CRUD
    ('/insert-chore-page', chore_handlers.InsertChorePage),
    ('/add-chore', chore_handlers.InsertChore),
    ('/edit-chore', chore_handlers.InsertChore),
    ('/delete-chore', chore_handlers.DeleteChore),
    ('/assign-chore', chore_handlers.AssignChore),
    ('/mark-chore', chore_handlers.MarkChore),


    # Members-CRUD
    ('/add-member', user_handlers.InsertMember),
    ('/edit-member', user_handlers.InsertMember),
    ('/delete-member', user_handlers.DeleteMember),
    ('/invite', user_handlers.Invite),

    # Notifier
    ('/notify')
], debug=True)

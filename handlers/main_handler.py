from handlers import base_handlers


class MainHandler(base_handlers.BasePage):
    def get_template(self):
        return "templates/groups.html"

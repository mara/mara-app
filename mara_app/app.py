"""
Flask app with auto-discovery of blueprints, cli commands etc.
"""

import gc

import click
import flask
from mara_app import config, layout
from mara_page import navigation, response, _
from werkzeug import exceptions


class MaraApp(flask.Flask):
    def __init__(self):
        super().__init__('mara')
        self.register_blueprints()
        self.register_commands()
        self.register_navigation_entries()
        self.register_page_layout()
        self.register_error_handlers()
        self.secret_key = '123'

    def register_blueprints(self):
        """Searches for all instances of flask.Blueprint and adds them to the app"""
        for blueprint in ([obj for obj in gc.get_objects() if isinstance(obj, flask.Blueprint)]):
            blueprint.static_url_path = '/static/_' + blueprint.name
            self.register_blueprint(blueprint)

    def register_commands(self):
        """Searches for all instances of click.Command and adds them to the app, grouped by package"""
        for command in ([obj for obj in gc.get_objects() if isinstance(obj, click.Command)]):
            if 'callback' in command.__dict__ and command.__dict__['callback']:
                package = command.__dict__['callback'].__module__.rpartition('.')[0]
                if package != 'flask':
                    command.name = package + '.' + command.name
                    self.cli.add_command(command)

    def register_navigation_entries(self):
        """Collects and merges all instances of NavigationEntry"""
        self.navigation_root = config.navigation_root()
        for navigation_entry in ([obj for obj in gc.get_objects() if isinstance(obj, navigation.NavigationEntry)]):
            if not navigation_entry.parent and navigation_entry != self.navigation_root:
                self.navigation_root.add_child(navigation_entry)

    def register_page_layout(self):
        """Adds a global layout with navigation etc. to pages"""

        def after_request(r: flask.Response):
            if isinstance(r, response.Response):
                r.set_data(layout.layout(r))
            return r

        self.after_request(after_request)

    def register_error_handlers(self):
        """Sets up error pages for all http exceptions"""

        def error_handler(error):
            if not isinstance(error, exceptions.HTTPException):
                error = exceptions.InternalServerError()
            return response.Response(_.span[_.p(style='color:#888')[error.description or ''],
                                            _.img(src=flask.url_for('mara_app.static', filename='mara.jpg'),
                                                  style='margin-top:30px;max-width:100%;')],
                                     title=error.name,
                                     status_code=error.code)

        for cls in exceptions.HTTPException.__subclasses__():
            self.register_error_handler(cls, error_handler)

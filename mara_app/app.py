"""
Flask app with auto-discovery of blueprints, cli commands etc.
"""

import copy
import functools
import sys
import typing

import flask
from mara_app import config, layout
from mara_page import navigation, response, _, bootstrap
from werkzeug import exceptions


class MaraApp(flask.Flask):
    def __init__(self):
        super().__init__('mara')
        self.register_blueprints()
        self.register_commands()
        self.register_navigation_entries()
        self.register_page_layout()
        self.register_error_handlers()
        self.disable_caching()
        self.patch_flask_url_for()
        self.config.update(config.flask_config())

    def register_blueprints(self):
        """Searches for all declared blueprints and adds them to the app"""
        for name, module in copy.copy(sys.modules).items():
            if 'MARA_FLASK_BLUEPRINTS' in dir(module):
                blueprints = getattr(module, 'MARA_FLASK_BLUEPRINTS')
                assert (isinstance(blueprints, typing.Iterable))
                for blueprint in blueprints:
                    assert (isinstance(blueprint, flask.Blueprint))
                    self.register_blueprint(blueprint)

    def register_commands(self):
        """Searches for all declared click commands and adds them to the app, grouped by package"""
        for name, module in copy.copy(sys.modules).items():
            if 'MARA_CLICK_COMMANDS' in dir(module):
                commands = getattr(module, 'MARA_CLICK_COMMANDS')
                assert (isinstance(commands, typing.Iterable))
                for command in commands:
                    if 'callback' in command.__dict__ and command.__dict__['callback']:
                        package = command.__dict__['callback'].__module__.rpartition('.')[0]
                        if package != 'flask':
                            command.name = package + '.' + command.name
                            self.cli.add_command(command)

    def register_navigation_entries(self):
        """Collects and merges all instances of NavigationEntry"""
        self.navigation_root = config.navigation_root()
        for name, module in copy.copy(sys.modules).items():
            if 'MARA_NAVIGATION_ENTRY_FNS' in dir(module):
                fns = getattr(module, 'MARA_NAVIGATION_ENTRY_FNS')
                assert (isinstance(fns, typing.Iterable))
                for fn in fns:
                    assert (isinstance(fn, typing.Callable))

                    navigation_entry = fn()
                    assert (isinstance(navigation_entry, navigation.NavigationEntry))
                    if not navigation_entry.parent and navigation_entry != self.navigation_root:
                        self.navigation_root.add_child(navigation_entry)

    def register_page_layout(self):
        """Adds a global layout with navigation etc. to pages"""

        def after_request(r: flask.Response):
            if isinstance(r, response.Response):
                r.set_data(layout.layout(r))
            return r

        self.after_request(after_request)

    def disable_caching(self):
        """
        Disable caching for dynamic content (not static files).
        See https://stackoverflow.com/questions/23112316/using-flask-how-do-i-modify-the-cache-control-header-for-all-output/37331139#37331139
        """

        def after_request(r: flask.Response):
            if 'Cache-Control' not in r.headers:
                r.headers['Cache-Control'] = 'no-store'
            return r

        self.after_request(after_request)

    def register_error_handlers(self):
        """Sets up error pages for all http exceptions"""

        def error_handler(error):
            if not isinstance(error, exceptions.HTTPException):
                error = exceptions.InternalServerError()
            return response.Response(bootstrap.card(body=_.span[_.p(style='color:#888')[error.description or ''],
                                                                _.img(src=flask.url_for('mara_app.static',
                                                                                        filename='mara.jpg'),
                                                                      style='margin-top:30px;max-width:100%;')]),
                                     title=f'{error.code}  {error.name}',
                                     status=error.code)

        for cls in exceptions.HTTPException.__subclasses__():
            self.register_error_handler(cls, error_handler)

    def patch_flask_url_for(self):
        """Caches calls to flask.url_for because it's kind of slow

        https://stackoverflow.com/questions/16713644/why-is-flask-url-for-too-slow"""
        original_url_for = flask.url_for
        flask.url_for = functools.lru_cache(maxsize=None)(original_url_for)

"""
Flask app with auto-discovery of blueprints, cli commands etc.
"""

import functools
import gc

import click
import flask
import sys
import typing
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
        self.patch_flask_url_for()
        self.secret_key = '123'
        self.config.update()

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
        for name, module in sys.modules.items():
            if 'MARA_NAVIGATION_ENTRY_FNS' in dir(module):
                fns = getattr(sys.modules['data_integration'], 'MARA_NAVIGATION_ENTRY_FNS')
                if not isinstance(fns, typing.Iterable):
                    raise ValueError(
                        f'MARA_NAVIGATION_ENTRY_FNS in module "{module.__name__}" is not bound to an array')
                for fn in fns:
                    if not isinstance(fn, typing.Callable):
                        raise ValueError(
                            f'{str(fn)} in MARA_NAVIGATION_ENTRY_FNS of module "{module.__name__}" is not a function')

                    navigation_entry = fn()
                    if not isinstance(navigation_entry, navigation.NavigationEntry):
                        raise ValueError(
                            f'Function {fn.__module__}.{fn.__name__} did not return an instance of NavigationEntry')
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
            return response.Response(bootstrap.card(body=_.span[_.p(style='color:#888')[error.description or ''],
                                                                _.img(src=flask.url_for('mara_app.static',
                                                                                        filename='mara.jpg'),
                                                                      style='margin-top:30px;max-width:100%;')]),
                                     title=error.name,
                                     status_code=error.code)

        for cls in exceptions.HTTPException.__subclasses__():
            self.register_error_handler(cls, error_handler)

    def patch_flask_url_for(self):
        """Caches calls to flask.url_for because it's kind of slow

        https://stackoverflow.com/questions/16713644/why-is-flask-url-for-too-slow"""
        original_url_for = flask.url_for
        flask.url_for = functools.lru_cache(maxsize=None)(original_url_for)

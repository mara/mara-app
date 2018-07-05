"""
Flask app with auto-discovery of blueprints, cli commands etc.
"""

import functools
import sys
import typing

import flask
from mara_app import config, layout
from mara_config import declare_config, get_contributed_functionality, init_mara_config_once
from mara_page import navigation, response, _, bootstrap
from werkzeug import exceptions


@declare_config()
def FEATURE_disable_register_all() -> bool:
    """A feature flag which can disable the old style registration of all imported modules"""
    return False


@declare_config()
def FEATURE_disable_mara_commands_in_flask() -> bool:
    """A feature flag which can disable the integration of MARA_CLICK_COMMANDS in the flask command"""
    return False


class MaraApp(flask.Flask):
    def __init__(self):
        super().__init__('mara')
        init_mara_config_once()
        if not FEATURE_disable_register_all():
            from mara_config import register_functionality_in_all_imported_modules
            register_functionality_in_all_imported_modules()
        if not FEATURE_disable_mara_commands_in_flask():
            self.register_commands()

        self.register_blueprints()
        self.register_navigation_entries()
        self.register_page_layout()
        self.register_error_handlers()

        self.disable_caching()
        self.patch_flask_url_for()
        self.config.update(config.flask_config())

    def register_blueprints(self):
        """Searches for all declared blueprints and adds them to the app"""

        for module, blueprint in get_contributed_functionality('MARA_FLASK_BLUEPRINTS'):
            assert (isinstance(blueprint, flask.Blueprint))
            self.register_blueprint(blueprint)

    def register_commands(self):
        """Searches for all declared click commands and adds them to the app, grouped by package"""
        for module, command in get_contributed_functionality('MARA_CLICK_COMMANDS'):
            if 'callback' in command.__dict__ and command.__dict__['callback']:
                package = command.__dict__['callback'].__module__.rpartition('.')[0]
                if package != 'flask':
                    command.name = package + '.' + command.name
                    self.cli.add_command(command)

    def register_navigation_entries(self):
        """Collects and merges all instances of NavigationEntry"""
        self.navigation_root = config.navigation_root()

        def all_children(navigation_entry: navigation.NavigationEntry) -> {navigation.NavigationEntry}:
            return functools.reduce(set.union, [all_children(child) for child in navigation_entry.children],
                                    set([navigation_entry]))

        # all navigation entries that have already been registered via `config.navigation_root`
        existing_navigation_entries = all_children(self.navigation_root)

        for module, fn in get_contributed_functionality('MARA_NAVIGATION_ENTRY_FNS'):
            assert (isinstance(fn, typing.Callable))
            navigation_entry = fn()
            assert (isinstance(navigation_entry, navigation.NavigationEntry))

            # only add navigation entries that have not been added yet via `config.navigation_root`
            if not navigation_entry in existing_navigation_entries and navigation_entry != self.navigation_root:
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

"""
Flask app with auto-discovery of blueprints, cli commands etc.
"""

import copy
import functools
import sys
import types
import typing

import click
import flask

from mara_app import config, layout
from mara_page import response, _, bootstrap, navigation
from werkzeug import exceptions


def module_functionalities(module: types.ModuleType, MARA_XXX: str, type) -> []:
    """
    Returns some functionalities of a module that is declared in a MARA_XXX variable or function

    `module.MARA_XXX` can be
    - a function that returns a list or dict
    - a list
    - a dict
    """
    if MARA_XXX in dir(module):
        functionalities = getattr(module, MARA_XXX)
        if isinstance(functionalities, typing.Callable):
            functionalities = functionalities()
        if isinstance(functionalities, typing.Dict):
            functionalities = functionalities.values()
        if not isinstance(functionalities, typing.Iterable):
            raise TypeError(
                f'{module.__name__}.{MARA_XXX} should be or return a list or dict of {type.__name__}. Got "{functionalities}".')
        for functionality in functionalities:
            if not isinstance(functionality, type):
                raise TypeError(f'In {module.__name__}.{MARA_XXX}: Expected a {type.__name__}, got "{functionality}"')
        return functionalities
    else:
        return []


class MaraApp(flask.Flask):
    def __init__(self):
        super().__init__('mara')
        self.register_blueprints()
        self.register_commands()
        self.register_page_layout()
        self.register_error_handlers()
        self.disable_caching()
        self.patch_flask_url_for()
        self.config.update(config.flask_config())

    def register_blueprints(self):
        """Searches for all declared blueprints and adds them to the app"""
        for module in copy.copy(sys.modules).values():
            for blueprint in module_functionalities(module, 'MARA_FLASK_BLUEPRINTS', flask.Blueprint):
                self.register_blueprint(blueprint)

    def register_commands(self):
        """Searches for all declared click commands and adds them to the app, grouped by package"""
        for module in copy.copy(sys.modules).values():
            for command in module_functionalities(module, 'MARA_CLICK_COMMANDS', click.Command):
                if 'callback' in command.__dict__ and command.__dict__['callback']:
                    package = command.__dict__['callback'].__module__.rpartition('.')[0]
                    if package != 'flask':
                        command.name = package + '.' + command.name
                        self.cli.add_command(command)

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


@functools.lru_cache(maxsize=None)
def combine_navigation_entries() -> navigation.NavigationEntry:
    """Collects and merges all instances of NavigationEntry"""
    navigation_root = config.navigation_root()

    def all_children(navigation_entry: navigation.NavigationEntry) -> {navigation.NavigationEntry}:
        return functools.reduce(set.union, [all_children(child) for child in navigation_entry.children],
                                set([navigation_entry]))

    # all navigation entries that have already been registered via `config.navigation_root`
    existing_navigation_entries = all_children(navigation_root)

    for module in copy.copy(sys.modules).values():
        for fn in module_functionalities(module,'MARA_NAVIGATION_ENTRY_FNS',typing.Callable):
            navigation_entry = fn()
            assert (isinstance(navigation_entry, navigation.NavigationEntry))

            # only add navigation entries that have not been added yet via `config.navigation_root`
            if not navigation_entry in existing_navigation_entries and navigation_entry != navigation_root:
                navigation_root.add_child(navigation_entry)

    return navigation_root
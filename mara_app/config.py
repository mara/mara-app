"""Application configuration"""

import flask
from mara_page import navigation
from mara_config import declare_config

@declare_config()
def flask_config() -> {str:str}:
    """
    Settings for the flask App.
    See http://flask.pocoo.org/docs/latest/config/#builtin-configuration-values for values and their defaults
    """
    return {'SECRET_KEY': '123-change-me-on-production'}


@declare_config()
def navigation_root() -> navigation.NavigationEntry:
    """
    The root of the navigation tree (only it's children will be displayed).
    All other defined entries that are not a child of entries in that list will be appended to that
    """
    return navigation.NavigationEntry(label='Root', children=[
        navigation.NavigationEntry(label='Home', uri_fn=lambda: '/', icon='home', rank=-1)
    ])


@declare_config()
def logo_url():
    """The location of the logo"""
    return flask.url_for('mara_app.static', filename='mara.jpg')


@declare_config()
def favicon_url():
    """The location of the favicon"""
    return flask.url_for('mara_app.static', filename='favicon.ico')

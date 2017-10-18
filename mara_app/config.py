"""Application configuration"""

import flask
from mara_page import navigation


def flask_config() -> {str: str}:
    """
    Settings for the flask App.
    See http://flask.pocoo.org/docs/latest/config/#builtin-configuration-values for values and their defaults
    """
    return {'SECRET_KEY': '123-change-me-on-production'}


def navigation_root() -> navigation.NavigationEntry:
    """
    The root of the navigation tree (only it's children will be displayed).
    All other defined entries that are not a child of entries in that list will be appended to that
    """
    return navigation.NavigationEntry(label='Root', children=[
        navigation.NavigationEntry(label='Home', uri_fn=lambda: '/', icon='home', rank=-1)
    ])


def logo_url():
    """The location of the logo"""
    return flask.url_for('mara_app.static', filename='mara.jpg')


def favicon_url():
    """The location of the favicon"""
    return flask.url_for('mara_app.static', filename='favicon.ico')

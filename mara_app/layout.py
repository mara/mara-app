"""Page layout of mara app"""

import functools
import re
import subprocess

import flask
import mara_page.response
from mara_app import config
from mara_page import navigation, _, xml


def layout(response: mara_page.response.Response) -> str:
    """Renders a complete html page for the response"""
    return '<!DOCTYPE html>\n' + str(
        _.html(lang='en')[
            _.head[
                head_elements(response)
            ],
            _.body(class_='navigation-collapsed')[
                body_elements(response)
            ]
        ])


def head_elements(response: mara_page.response.Response) -> [xml.XMLElement]:
    """All elements in the head section of the html page"""
    return [
        _.meta(charset='utf-8'),
        _.meta(name='viewport', content='width=device-width, initial-scale=1, shrink-to-fit=no'),
        _.title[re.sub(r'<[^>]*?>', '', str(xml.render(response.title)))],
        [_.link(rel='stylesheet', href=url + '?' + _current_git_commit())[''] for url in css_files(response)],
        _.link(rel='icon', type='image/png', href=config.favicon_url() + '?' + _current_git_commit())
    ]


def body_elements(response: mara_page.response.Response) -> [xml.XMLElement]:
    """All elements inside the body section of the html page"""
    return [
        _.script['var isTouchDevice = ("ontouchstart" in document.documentElement); ',
                 'window.document.getElementsByTagName("body")[0].className += isTouchDevice ? " touch" : " no-touch";'],
        page_header(response),
        navigation_bar(),
        content_area(response),
        [_.script(src=url + '?' + _current_git_commit())[''] for url in js_files(response)],
        flash_messages(response)
    ]


def css_files(response: mara_page.response.Response) -> [xml.XMLElement]:
    """The list of all css files to include in the page"""
    return [flask.url_for('mara_app.static', filename='bootstrap-4.0.0-alpha.6/bootstrap.min.css'),
            flask.url_for('mara_app.static', filename='font-awesome-4.7.0/css/font-awesome.min.css'),
            flask.url_for('mara_app.static', filename='tether-1.3.3/tether.min.css'),
            flask.url_for('mara_app.static', filename='mara.css')
            ] + response.css_files


def js_files(response: mara_page.response.Response):
    """The list of all js files to include in the page"""
    return [flask.url_for('mara_app.static', filename='jquery-3.1.1.min.js'),
            flask.url_for('mara_app.static', filename='tether-1.3.3/tether.min.js'),
            flask.url_for('mara_app.static', filename='bootstrap-4.0.0-alpha.6/bootstrap.min.js'),
            flask.url_for('mara_app.static', filename='mara.js')
            ] + response.js_files


def page_header(response: mara_page.response.Response):
    """Renders the fixed top part of the page"""
    return _.nav(id='mara-page-header', class_='navbar fixed-top')[
        _.a(class_='navigation-toggle-button fa fa-lg fa-reorder', onclick='toggleNavigation()')[' '],
        _.h1()[response.title],
        _.img(src=config.logo_url() + '?' + _current_git_commit()),
        _.span(class_='action-buttons')[map(action_button, response.action_buttons)]]


def action_button(button: mara_page.response.ActionButton):
    """Renders an action button"""
    return [_.a(class_='btn', href=button.action, title=button.title)[
                _.span(class_='fa fa-' + button.icon)[''], ' ',
                button.label]]

@functools.lru_cache(maxsize=None)
def navigation_bar() -> str:
    """Renders the navigation sidebar"""

    def render_entries(entries: [navigation.NavigationEntry] = [], level: int = 1):
        def render_entry(entry: navigation.NavigationEntry, level: int = 1):
            attrs = {}
            if entry.children:
                attrs.update({'onClick': 'toggleNavigationEntry(this)'})
            else:
                attrs.update({'onClick': 'highlightNavigationEntry(\'' + entry.uri_fn() + '\');',
                              'href': entry.uri_fn()})

            if entry.description:
                attrs.update({'title': entry.description, 'data-toggle': 'tooltip',
                              'data-container': 'body', 'data-placement': 'right'})
            return _.div(class_='mara-nav-entry level-' + str(level),
                         style='display:none' if level > 1 else '')[
                _.a(**attrs)[
                    _.div(class_='mara-nav-entry-icon fa fa-fw fa-' + entry.icon + (' fa-lg' if level == 1 else ''))[
                        ''] if entry.icon else '',
                    _.div(class_='mara-nav-entry-text')[entry.label.replace('_', '_<wbr>')],
                    _.div(class_='mara-caret fa fa-caret-down')[''] if entry.children else ''],
                render_entries(entry.children, level + 1)
            ]

        return [functools.partial(render_entry, level=level)(entry)
                for entry in sorted([entry for entry in entries if entry.visible], key=lambda x: x.rank)]

    return str(_.nav(id='mara-navigation', class_='nav')[render_entries(flask.current_app.navigation_root.children)])


def content_area(response: mara_page.response.Response) -> xml.XMLElement:
    """Renders the main content area"""
    return _.div(id='mara-main', class_='container-fluid')[response.response]


def flash_messages(response: mara_page.response.Response) -> xml.XMLElement:
    """Displays flask flash messages"""
    return [_.div(id='alerts'),
            _.script(type='text/javascript')[
                map(lambda m: 'showAlert("' + m[1].replace('"', '&quot;') + '","' + (
                    m[0] if m[0] != 'message' else 'info') + '");',
                    flask.get_flashed_messages(True))

            ]]


@functools.lru_cache(maxsize=None)
def _current_git_commit():
    """Returns the current git commit of the mara application"""
    command = f'git --git-dir {flask.current_app.root_path}/.git rev-parse HEAD'
    return subprocess.getoutput(command)

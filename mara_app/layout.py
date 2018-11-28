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
            _.body[
                body_elements(response)
            ]
        ]
    )


def head_elements(response: mara_page.response.Response) -> [xml.XMLElement]:
    """All elements in the head section of the html page"""
    return [
        _.meta(charset='utf-8'),
        _.meta(name='viewport', content='width=device-width, initial-scale=1, shrink-to-fit=no'),
        _.title[re.sub(r'<[^>]*?>', '', ''.join(xml.render(response.title)))],
        [_.link(rel='stylesheet', href=url + ('&' if '?' in  url else '?') + _current_git_commit())['']
         for url in css_files(response)],
        _.link(rel='icon', type='image/png', href=config.favicon_url() + '?' + _current_git_commit())
    ]


def body_elements(response: mara_page.response.Response) -> [xml.XMLElement]:
    """All elements inside the body section of the html page"""
    return [
        _.div(class_="layout", id="layout")[
            _.div(class_="layout__header")[
                page_header(response),
            ],
            _.div(class_="layout__navigation")[
                navigation_bar(),
            ],
            _.div(class_="layout__filters")[
                filter_panel(response),
            ],
            _.div(class_="layout__content")[
                content_area(response),
            ],
            [
                _.script(src=url + '?' + _current_git_commit())[''] for url in js_files(response)
            ],
            _.div(class_="layout__alerts")[
                flash_messages(response)
            ],
            _.script[f'''
document.addEventListener("DOMContentLoaded", function(){{
    Layout("layout");
}});'''
            ]
        ]
    ]


def css_files(response: mara_page.response.Response) -> [xml.XMLElement]:
    """The list of all css files to include in the page"""
    return [
        'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'https://use.fontawesome.com/releases/v5.4.2/css/solid.css',
        'https://use.fontawesome.com/releases/v5.4.2/css/fontawesome.css',
        flask.url_for('mara_app.static', filename='mara.css')
    ] + response.css_files


def js_files(response: mara_page.response.Response):
    """The list of all js files to include in the page"""
    return [
        'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js',
        'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js',
        flask.url_for('mara_app.static', filename='vendor/jquery.floatThead.2.0.3.min.js'),
        flask.url_for('mara_app.static', filename='mara.js')
    ] + response.js_files


def page_header(response: mara_page.response.Response):
    """Renders the fixed top part of the page"""
    return _.nav(id='page-header', class_='page-header')[
        _.button(
            class_='page-header__menu js-page-header__menu',
            onclick='toggleNavigation(event)'
        )[
            _.span(class_='page-header__menu-inner')
        ],
        _.img(
            class_='page-header__logo',
            src=config.logo_url() + '?' + _current_git_commit()
        ),
        _.div(class_='page-header__actions')[
            map(action_button, response.action_buttons),
            _.div(class_='page-header__filters')[
                _.button(
                    class_='mara-button',
                    onclick='toggleFilters()'
                )[
                    'Filters',
                    _.span(class_="mara-button__icon")[
                        _.span(class_="fa fa-filter")['']
                    ]
                ]
            ] if response.filter_panel else ''
        ]
    ]


def action_button(button: mara_page.response.ActionButton):
    """Renders an action button"""
    return [
        _.a(href=button.action, title=button.title)[
            _.span(class_='fa fa-' + button.icon)[''], ' ',
            button.label
        ]
    ]

def navigation_bar() -> str:
    """Renders the navigation sidebar"""

    # the navigation bar content is loaded asynchronously.
    # Until that happens, the previous version from local storage is displayed
    return [
        _.nav(id='mara-navigation', class_='mara-navigation')[' '],
        _.script[
    """
(function () {
    var navigationEntries = localStorage.getItem('navigation-bar');
    if (navigationEntries) {
        document.getElementById('mara-navigation').innerHTML = navigationEntries;
    }
})();
"""
        ]
    ]

def filter_panel(response: mara_page.response.Response) -> xml.XMLElement:
    return _.div(id='mara-filter-panel', class_='mara-filters')[
        response.filter_panel
    ]

def content_area(response: mara_page.response.Response) -> xml.XMLElement:
    """Renders the main content area"""
    return _.div(id='mara-main')[
        _.div(class_="mara-main__header")[
            _.h1[response.title],
        ],
        response.response
    ]


def flash_messages(response: mara_page.response.Response) -> xml.XMLElement:
    """Displays flask flash messages"""
    return [
        _.div(id='alerts'),
        _.script(type='text/javascript')[
            map(lambda m: 'showAlert("' + m[1].replace('"', '&quot;') + '","' + (
                m[0] if m[0] != 'message' else 'info') + '");',
                flask.get_flashed_messages(True))

        ]
    ]


@functools.lru_cache(maxsize=None)
def _current_git_commit():
    """Returns the current git commit of the mara application"""
    command = f'git --git-dir {flask.current_app.root_path}/.git rev-parse HEAD'
    status, output = subprocess.getstatusoutput(command)
    return output if status == 0 else ''

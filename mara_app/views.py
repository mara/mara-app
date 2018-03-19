"""Mara admin views"""

import copy
import functools
import html
import inspect
import pprint
import sys
import types
import typing

import flask

from mara_app import monkey_patch
from mara_page import acl, navigation, response, _, bootstrap, xml

blueprint = flask.Blueprint('mara_app', __name__, url_prefix='/mara-app', static_folder='static')

acl_resource = acl.AclResource('Configuration')


def _config_modules(with_functions=True):
    """Gathers all configuration modules and their functions"""
    config_modules = {}
    for name, module in copy.copy(sys.modules).items():
        if 'MARA_CONFIG_MODULES' in dir(module):
            modules = getattr(module, 'MARA_CONFIG_MODULES')
            assert (isinstance(modules, typing.Iterable))
            for config_module in modules:
                assert (isinstance(config_module, types.ModuleType))
                config_modules[config_module.__name__] = {'doc': config_module.__doc__, 'functions': {}}

                if with_functions:
                    for member_name, member in config_module.__dict__.items():
                        if inspect.isfunction(member):
                            try:
                                value = member()
                            except Exception:
                                value = 'error calling function'

                            new_function = monkey_patch.REPLACED_FUNCTIONS.get(
                                config_module.__name__ + '.' + member_name, '')

                            config_modules[config_module.__name__]['functions'][member_name] \
                                = {'doc': member.__doc__ or '', 'value': value, 'new_function': new_function}
    return config_modules


@blueprint.route('/configuration')
def configuration_page():
    # gather all config functions by package

    current_user_has_permission = acl.current_user_has_permission(acl_resource)

    return response.Response(
        html=[(bootstrap.card(id=module_name,
            header_left=html.escape(module_name),
            body=[_.p[_.em[html.escape(str(config['doc']))]],
                  bootstrap.table(
                      [],
                      [_.tr[
                           _.td[_.tt[html.escape(function_name).replace('_', '_<wbr/>')],
                                [_.br, ' ⟵ ', _.tt[html.escape(function['new_function'])
                                    .replace('.', '<wbr/>.').replace('_', '_<wbr/>')]]
                                if function['new_function'] else ''],
                           _.td[_.em[html.escape(function['doc'])]],
                           _.td[
                               _.pre[html.escape(pprint.pformat(function['value']))]
                               if current_user_has_permission
                               else acl.inline_permission_denied_message()
                           ]] for function_name, function in config['functions'].items()])
                  ]) if config['functions'] else '')
              for module_name, config in sorted(_config_modules().items())],
        title='Mara Configuration')


def navigation_entry():
    return navigation.NavigationEntry(
        label='Package Configs', icon='cogs', rank=100,
        description='Package config functions with project replacements',
        uri_fn=lambda: flask.url_for('mara_app.configuration_page'),
        children=[
            navigation.NavigationEntry(
                label=module_name, icon='list',description=config['doc'],
                uri_fn=lambda _module_name=module_name: flask.url_for('mara_app.configuration_page',_anchor=_module_name))
            for module_name, config in sorted(_config_modules().items())]
    )


@blueprint.route('/navigation-bar')
@functools.lru_cache(maxsize=None)
def navigation_bar() -> [str]:
    # The navigation sidebar is loaded asynchronously for better rendering experience
    def render_entries(entries: [navigation.NavigationEntry] = [], level: int = 1):
        def render_entry(entry: navigation.NavigationEntry, level: int = 1):
            attrs = {}
            if entry.children:
                attrs['onClick'] = 'toggleNavigationEntry(this)'
            else:
                attrs['href'] = entry.uri_fn()

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

    return flask.Response(''.join(list(xml.render(render_entries(flask.current_app.navigation_root.children)))))

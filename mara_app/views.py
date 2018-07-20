"""Mara admin views"""

import functools
import html

import flask
from mara_config.config_system.config_display import get_config_for_display
from mara_page import acl, navigation, response, _, bootstrap, xml

blueprint = flask.Blueprint('mara_app', __name__, url_prefix='/mara-app', static_folder='static')

acl_resource = acl.AclResource('Configuration')


@blueprint.route('/configuration')
def configuration_page():
    config = get_config_for_display()
    current_user_has_permission = acl.current_user_has_permission(acl_resource)

    return response.Response(
        html=[(bootstrap.card(id=module_name,
                              header_left=html.escape(module_name),
                              body=[_.p[_.em[html.escape(str(module_content.doc))]],
                                    bootstrap.table(
                                        [],  # no headers
                                        [_.tr[
                                             _.td[
                                                 _.tt[html.escape(config_name).replace('_', '_<wbr/>')],
                                                 (
                                                     [_.br, ' ⟵ ', _.tt[html.escape(config_function.func_desc)
                                                         .replace('.', '<wbr/>.').replace('_', '_<wbr/>')]]
                                                 ) if config_function.set_func else (
                                                     _.strong[' (UNSET BUT NEEDS TO BE SET!)']
                                                     if config_function.needs_set else
                                                     ''
                                                 )
                                             ],
                                             _.td[_.em[html.escape(config_function.doc)]],
                                             _.td[
                                                 _.pre[
                                                     html.escape(config_function.value_desc)
                                                 ]
                                                 if current_user_has_permission
                                                 else acl.inline_permission_denied_message()
                                             ]
                                         ] for config_name, config_function in module_content.items()])
                                    ]) if module_content.config_functions else '')
              for module_name, module_content in config.items()],
        title='Mara Configuration')


def navigation_entry():
    config = get_config_for_display()

    return navigation.NavigationEntry(
        label='Package Configs', icon='cogs', rank=100,
        description='Package config functions with project replacements',
        uri_fn=lambda: flask.url_for('mara_app.configuration_page'),
        children=[
            navigation.NavigationEntry(
                label=module_name, icon='list', description=module_content.doc,
                uri_fn=lambda _module_name=module_name: flask.url_for('mara_app.configuration_page',
                                                                      _anchor=_module_name))
            for module_name, module_content in sorted(config.items())]
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

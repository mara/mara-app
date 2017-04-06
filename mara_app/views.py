"""Mara admin views"""

import html
import inspect
import pathlib
import pprint
import sys

from mara_page import navigation, response, _

import flask

mara_app = flask.Blueprint('mara_app', __name__, url_prefix='/admin', static_folder='static')


@mara_app.route('/configuration')
def configuration_page():
    # gather all config functions by package
    config_modules = {}
    package_path = str(pathlib.Path(__file__).parent.parent.parent)
    app_path = str(pathlib.Path(__file__).parent.parent.parent.parent / 'app')
    for module_name, module in sys.modules.items():
        if (hasattr(module, '__file__')) and (module.__file__.startswith(package_path) or module.__file__.startswith(app_path)) \
                and module_name.split('.')[-1] == 'config':
            if not module_name in config_modules:
                config_modules[module_name] = {'doc': module.__doc__, 'functions': {}}

            for member_name, member in module.__dict__.items():
                if inspect.isfunction(member) and member.__module__ == module_name:
                    value = ''
                    try:
                        value = member()
                    except TypeError:
                        value = 'error calling function'

                    config_modules[module_name]['functions'][member_name] \
                        = {'doc': member.__doc__ or '', 'value': value}

    def render_function(function_name, function):
        return _.tr[
            _.td(style='max-width:15%;')[_.div(style='display:block;overflow:hidden;text-overflow:ellipsis')[
                function_name.replace('_', '_<wbr/>')]],
            _.td(style='width:30%')[_.em[function['doc']]],
            _.td(style='width:55%;')[
                _.pre(style='margin:0px;padding-top:3px;overflow:hidden;text-overflow:ellipsis;')[
                    html.escape(pprint.pformat(function['value']))]],
        ]

    def render_module(module_name, config):
        return [_.h3[module_name], _.p[str(config['doc'])],
                _.table(_class='table table-hover table-sm', style='table-layout:fixed')[
                    [render_function(function_name, function) for function_name, function in
                     config['functions'].items()]]]

    return response.Response(
        [render_module(module_name, config) for module_name, config in sorted(config_modules.items())],
        title='Mara Configuration')


navigation_entry = navigation.NavigationEntry('Configuration',
                                              uri_fn=lambda: flask.url_for('mara_app.configuration_page'),
                                              icon='cogs', rank=100)

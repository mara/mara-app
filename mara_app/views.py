"""Mara admin views"""

import html
import inspect
import pathlib
import pprint
import sys

from mara_page import acl

import flask
from mara_page import navigation, response, _, bootstrap

mara_app = flask.Blueprint('mara_app', __name__, url_prefix='/admin', static_folder='static')

acl_resource = acl.AclResource('Configuration')


@mara_app.route('/configuration')
@acl.require_permission(acl_resource)
def configuration_page():
    # gather all config functions by package
    config_modules = {}
    package_path = str(pathlib.Path(__file__).parent.parent.parent)
    app_path = str(pathlib.Path(__file__).parent.parent.parent.parent.joinpath('app'))
    for module_name, module in list(sys.modules.items()):
        if (hasattr(module, '__file__')) and (
                    module.__file__.startswith(package_path) or module.__file__.startswith(app_path)) \
                and module_name.split('.')[-1] == 'config':
            if not module_name in config_modules:
                config_modules[module_name] = {'doc': module.__doc__, 'functions': {}}

            for member_name, member in module.__dict__.items():
                if inspect.isfunction(member) and member.__module__ == module_name:
                    value = ''
                    try:
                        value = member()
                    except Exception:
                        value = 'error calling function'

                    config_modules[module_name]['functions'][member_name] \
                        = {'doc': member.__doc__ or '', 'value': value}

    return response.Response(
        html=[(bootstrap.card(
            header_left=html.escape(module_name),
            body=[_.p[_.em[html.escape(str(config['doc']))]],
                  bootstrap.table(
                      [],
                      [_.tr[
                           _.td[function_name.replace('_', '_<wbr/>')],
                           _.td[_.em[function['doc']]],
                           _.td[_.pre[html.escape(pprint.pformat(function['value']))]]]
                       for function_name, function in config['functions'].items()])
                  ]) if config['functions'] else '') for module_name, config in
              sorted(config_modules.items())],
        title='Mara Configuration')


navigation_entry = navigation.NavigationEntry('Configuration',
                                              uri_fn=lambda: flask.url_for('mara_app.configuration_page'),
                                              icon='cogs', rank=100)

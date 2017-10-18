"""Mara admin views"""

import html
import inspect
import pathlib
import pprint
import sys
import copy

import flask, typing, types
from mara_page import acl
from mara_page import navigation, response, _, bootstrap

blueprint = flask.Blueprint('mara_app', __name__, url_prefix='/admin', static_folder='static')

acl_resource = acl.AclResource('Configuration')

@blueprint.route('/configuration')
@acl.require_permission(acl_resource)
def configuration_page():
    # gather all config functions by package
    config_modules = {}
    for name, module in copy.copy(sys.modules).items():
        if 'MARA_CONFIG_MODULES' in dir(module):
            modules = getattr(module, 'MARA_CONFIG_MODULES')
            assert(isinstance(modules, typing.Iterable))
            for config_module in modules:
                assert(isinstance(config_module, types.ModuleType))
                config_modules[config_module.__name__] = {'doc': config_module.__doc__, 'functions': {}}

                for member_name, member in config_module.__dict__.items():
                    if inspect.isfunction(member) and member.__module__ == config_module.__name__:
                        try:
                            value = member()
                        except Exception:
                            value = 'error calling function'

                        config_modules[config_module.__name__]['functions'][member_name] \
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


def navigation_entry():
    return navigation.NavigationEntry('Configuration',
                                      uri_fn=lambda: flask.url_for('mara_app.configuration_page'),
                                      icon='cogs', rank=100)

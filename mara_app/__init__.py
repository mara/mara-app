"""Make the functionalities of this package auto-discoverable by mara-app"""
__version__ = '2.5.0'


def MARA_CONFIG_MODULES():
    from . import config
    return [config]


def MARA_FLASK_BLUEPRINTS():
    from . import views
    return [views.blueprint]


def MARA_AUTOMIGRATE_SQLALCHEMY_MODELS():
    return []


def MARA_ACL_RESOURCES():
    from . import views
    return {'Configuration': views.acl_resource}


def MARA_CLICK_COMMANDS():
    return []


def MARA_NAVIGATION_ENTRIES():
    from . import views
    return {'Package Configs': views.package_configs_navigation_entry()}

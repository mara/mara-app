from mara_app import views, cli, config

MARA_CONFIG_MODULES = [config]

MARA_FLASK_BLUEPRINTS = [views.blueprint]

MARA_AUTOMIGRATE_SQLALCHEMY_MODELS = []

MARA_ACL_RESOURCES = [views.acl_resource]

MARA_CLICK_COMMANDS = [cli.migrate]

MARA_NAVIGATION_ENTRY_FNS = [views.navigation_entry]

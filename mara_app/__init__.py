def MARA_CONFIG_MODULES():
    import mara_app.config
    return [mara_app.config]

def MARA_FLASK_BLUEPRINTS():
    from mara_app import views
    return [views.blueprint]

def MARA_ACL_RESOURCES():
    from mara_app import views
    return [views.acl_resource]

def MARA_NAVIGATION_ENTRY_FNS():
    from mara_app import views
    return [views.navigation_entry]

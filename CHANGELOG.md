# Changelog

## 1.3.0
*2017-10-18*

- Monkey patching function logs the changes being applied and list them when calling `monkey_patch.list_patches()`, allowing for an optional description


## 1.2.0
*2017-09-21*

- Changed discovery of blueprints, commands, navigation entries etc. from inspecting gc to explicit module inventories
- Automatic creation of mara backend db if it does not exist in migrations
- Performance improvements in response rendering
- Improved css for cards, tables, page headers 
- Added floating of table headers
- Fix for setting flask app configuration
- Other minor fixes

**required changes**

- requires update of [mara-page](https://github.com/mara/mara-page) to at least 1.2.0
- packages now need to explicitly declare which blueprints, commands, sql alchemy models etc. should be registered by `mara_app`. Example: the [`__init__.py`](https://github.com/mara/mara-app/blob/master/mara_app/__init__.py) from this package:
 
```python
from mara_app import views, cli, config

MARA_CONFIG_MODULES = [config]

MARA_FLASK_BLUEPRINTS = [views.blueprint]

MARA_AUTOMIGRATE_SQLALCHEMY_MODELS = []

MARA_ACL_RESOURCES = [views.acl_resource]

MARA_CLICK_COMMANDS = [cli.migrate]

MARA_NAVIGATION_ENTRY_FNS = [views.navigation_entry]

```


## 1.1.0
*2017-05-24*

- Improved navigation side bar
- Git commit of app appended to asset urls (e.g. `styles.css?efcfbaddfa4a..`)
- Decreased font size to 12px
- Anchor offsetting via `.anchor` css class
- Config page beautifications
- Navigation entries can be hidden by setting `visible=False`


## 1.0.4
*2017-04-15* 

- minor improvements for _/admin/configuration_ page


## 1.0.3
*2017-04-05*

- migrations work without activating the virtualenv first
- improved updating of virtualenvs


## 1.0.2
*2017-03-29*

- Configuration improvements: frontend only displays config modules in `packages` folder, started flask config 


## 1.0.0 - 1.0.1
*2017-03-12* 

- Initial version plus bug fixes

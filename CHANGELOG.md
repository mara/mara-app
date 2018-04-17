# Changelog

## 1.5.0 - 1.5.1 (2018-04-08)

- Move auto-migrate feature to mara-db package
- cope with absense of local git checkout in layout._current_git_commit
- Wipe incompatible local copies when pip installing packages 



## 1.4.0 - 1.4.3 (2018-01-29)

- Add new Makefile target `check-for-newer-package-versions` which list all packages that have newer tags than the current checkout
- Always check for newer package versions in `make update-packages`
- make `divHeightKey` optional in `loadContentAsynchronously`
- bug fixes for auto-migration
- bug fixes for monkey patching
- improve configuration page
 


## 1.3.0 - 1.3.6 (2017-12-30)

- modularize Makefile and stop overwriting project Makefile from package 
- asynchronous loading of navigation bar for better page rendering experience
- store height of asynchronously loaded content in local storage for improved rendering experience
- show a list of all patched and wrapped functions in /configuration page 
- improve configuration ui
- add error handling for asynchronous loading of navigation 
- use MARA_AUTOMIGRATE_SQLALCHEMY_MODELS for finding sqlalchemy models (instead of walking through GC)
- add workaround for failing pip on Ubuntu/Debian (#22)
- fix dependency links
- improvements around navigation tree
- Allow disabling makeshell in make targets (by prepending DISABLE_MAKESHELL)
- provide hints and make target for running flask threaded

**required changes**

- Copy `mara-app/.scripts` directory to `.scripts/mara-app` in project code (will be updated automatically)
- Include mara Makefiles in Project Makefile:

```
# output coloring & timing
include .scripts/mara-app/init.mk

# virtual env creation, package updates, db migration
include .scripts/mara-app/install.mk

# ... your own stuff
```


## 1.2.0 - 1.2.1 (2017-09-21)

- Changed discovery of blueprints, commands, navigation entries etc. from inspecting gc to explicit module inventories
- Automatic creation of mara backend db if it does not exist in migrations
- Performance improvements in response rendering
- Improved css for cards, tables, page headers 
- Added floating of table headers
- Fix for setting flask app configuration
- Other minor fixes
- Bug fix: auto-migration did not execute multiple changes per table

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


## 1.1.0 (2017-05-24)

- Improved navigation side bar
- Git commit of app appended to asset urls (e.g. `styles.css?efcfbaddfa4a..`)
- Decreased font size to 12px
- Anchor offsetting via `.anchor` css class
- Config page beautifications
- Navigation entries can be hidden by setting `visible=False`



## 1.0.0 - 1.0.4 (2017-03-12) 

- Initial version plus bug fixes
- Configuration improvements: frontend only displays config modules in `packages` folder, started flask config 
- migrations work without activating the virtualenv first
- improved updating of virtualenvs
- minor improvements for _/admin/configuration_ page

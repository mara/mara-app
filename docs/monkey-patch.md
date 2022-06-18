Monkey patching
===============

With the monkey patch it is possible to override default behavior inside the Mara ETL framework.
It can be used for whatever function is avialble.

```{note}
Be aware of that not all functions are designed to be patched and might become
obsolete, might be removed or change their behavior in upcoming versions.

Pay close attention to the changelog and code changes while upgrading to newer package versions.
```

Patching the config
-------------------

Configuration values are typically defined as functions to support maximum flexibility. To override
their default behavior you can patch them like this:

``` python
from mara_app.monkey_patch import patch
import mara_pipelines.config

# changes the default db alias for pipelines from "dwh-etl" to "dwh"
#
# this is done by using the patch as an attribute on a new function
# returning the wished value
@patch(mara_pipelines.config.default_db_alias)
def default_db_alias():
    return 'dwh'

# changes the max. number of parallel tasks to 16.
#
# this is done by using the patch on a lambda function
patch(mara_pipelines.config.max_number_of_parallel_tasks)(lambda: 16)
```

API
===

.. module:: mara_app

This part of the documentation covers all the interfaces of Mara App. For
parts where the package depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


App
---

.. module:: mara_app.app

.. autoclass:: MaraApp
    :special-members: __init__
    :members:

.. autofunction:: module_functionalities


Monkey patch
------------

.. module:: mara_app.monkey_patch

.. autofunction:: patch

.. autofunction:: wrap

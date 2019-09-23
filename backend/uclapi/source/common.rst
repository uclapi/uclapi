Common
=================

This module contains common code which is used across all the modules, with examples
including response objects and our own custom decorators.


Contents
-------------------------
.. toctree::
   common

decorators.py
-------------
This module contains everything needed for our uclapi_protected_endpoint decorator
to work.

.. automodule:: common.decorators
   :members:
   :undoc-members:
   :private-members:
   :exclude-members: uclapi_protected_endpoint

.. autodecorator:: common.decorators.uclapi_protected_endpoint

helpers.py
----------
This module contains general helper functions such as JSON and rate limited HTTP responses, token generation and such.

.. automodule:: common.helpers
   :members:
   :undoc-members:
   :private-members:

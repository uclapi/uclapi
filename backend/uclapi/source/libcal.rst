LibCal
=========================
This module contains all the code relating to the LibCal endpoints.

Contents
-------------------------
.. toctree::
   libcal

Design
-------------------------
This set of API proxies the LibCal API, used to book rooms and seats for both individual and group use.

Currently we only support the read-only endpoints but it is intended to also present endpoints that allow creating and
cancelling bookings.

To allow read access to personal data, a new OAuth scope is introduced - ``libcal_read``.

The design is quite simple, we simply proxy the requests from the client to LibCal, and give the results back from
LibCal back to the client.

OAuth tokens last for an hour and seem to be infinitely refreshable. For simplicity, a management command is added that
refreshes the token used during proxying. It is recommended that a systemd timer or a cron job is used to run this
command every 30 mins, to minimise the chances of us not having a token at any moment during proxying.

Bookings made via the web UI use ``User.mail`` as the email address and is also the unique identifier used to show/create
bookings, however this was only stored in our DB recently when ``12a5a9896c96c4a268815cf39d3798bbb417ea47`` was merged.
Seeming as the ``User`` model is only updated when the user goes through the Shibboleth workflow, this presented a
problem as ``User.mail`` would likely be empty. Fortunately, one can get around this problem by noticing that as a new
scope is required for accessing personal LibCal data, the user would have to go through the Shibboleth process to
approve the app's request for the new scope, at which point ``User.mail`` would be updated.

views.py
--------------------

.. automodule:: libcal.views
   :members:
   :undoc-members:
   :private-members:

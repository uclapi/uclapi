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

Currently we only support the read-only endpoints that do not display any personally identifiable information but it is
intended to also present endpoints that allow creating and cancelling bookings, as well as viewing the bookings of a
specific user.

The design is quite simple, we simply proxy the requests from the client to LibCal, and give the results back from
LibCal back to the client.

OAuth tokens last for an hour and seem to be infinitely refreshable. For simplicity, a management command is added that
refreshes the token used during proxying. It is recommended that a systemd timer or a cron job is used to run this
command every 30 mins, to minimise the chances of us not having a token at any moment during proxying.

views.py
--------------------

.. automodule:: libcal.views
   :members:
   :undoc-members:
   :private-members:

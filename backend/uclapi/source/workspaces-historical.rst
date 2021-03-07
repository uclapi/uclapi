Workspaces Historical
=====================
An extension to the workspaces module to add SurveysList, SensorsList, and HistoricalList. This allows for developers
to access the full history for any seat across any of the libraries. Importantly this is the first use of **Django Rest
Framework** to directly provide an API view.

Archive
-------
The OccupEye endpoint is very slow to access and unlike the original workspaces there is too much data to store in
Redis. Instead all historical endpoints are stored in the main UCL API Postgres database (see below). Everyday at 2am
a cron job runs the feed_occupeye_archive which executes the OccupEyeArchive. This adds the last 24 hours to the uclapi
database. The task goes through the following stages:

1. Cross check the survey locations to see if anything has changed or been added.
2. For each survey location fetch all the sensors and data points since the last_updated time.
3. Calculate the deltas for each sensor and insert into the database.

Database
--------
Each survey location (library) has a collection of sensors (seats) associated with it. The surveys are stored inside
the workspaces_surveys table including a survey_id, name, active, start_datetime (the date the survey was first in
use), end_datetime (the date the survey was either deprecated or planned to be deprecated), and last_updated (the
date when the cronjob archive last ran successfully for that particular survey location. Each sensor has an id,
sensor_id (id in OccupEye, not necessarily unique), survey_id (survey associated with this id), hardware_id, and
survey_device_id (the final two of which are exposed but not well documented in the OccupEye docs).

However surveys and sensors sometimes change, these changes are recorded in workspaces_surveychanges and
workspaces_sensorreplacements. Changes are rare and most commonly it involves extending the end_datetime of a survey
location. There is currently only one sensor replacement.

Finally the historical data is stored within workspaces_historical. This is stored as deltas (only the datetime of
the change of state is saved, with the in-between values interpolated). The API provides updates on a 10 minute
frequency hwoever only around 1/20 of these values are stored.

Tests
-----
Archive tests uses a mocked endpoint which returns values from the tests_*.json files. Importantly the
FIRST_OCCUPEYE_INSTALLATION date is patched in and times frozen with freezegun.


occupeye/archive.py
-------------------

.. automodule:: workspaces.occupeye.archive
    :members:
    :undoc-members:
    :private-members:


occupeye/endpoint.py
--------------------

.. automodule:: workspaces.occupeye.endpoint
    :members:
    :undoc-members:
    :private-members:
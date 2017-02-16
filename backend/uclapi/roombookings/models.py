from __future__ import unicode_literals

from django.db import models
from .api_helpers import generate_token
import json


class Booking(models.Model):
    setid = models.CharField(max_length=40, blank=True, null=True)
    siteid = models.CharField(max_length=40, blank=True, null=True)
    roomid = models.CharField(max_length=160, blank=True, null=True)
    sitename = models.CharField(max_length=320, blank=True, null=True)
    roomname = models.CharField(max_length=320, blank=True, null=True)
    bookabletype = models.CharField(max_length=40, blank=True, null=True)
    slotid = models.BigIntegerField(primary_key=True)
    bookingid = models.CharField(max_length=80, blank=True, null=True)
    starttime = models.CharField(max_length=80, blank=True, null=True)
    finishtime = models.CharField(max_length=20, blank=True, null=True)
    startdatetime = models.DateField(blank=True, null=True)
    finishdatetime = models.DateField(blank=True, null=True)
    weeknumber = models.FloatField(blank=True, null=True)
    condisplayname = models.CharField(max_length=4000, blank=True, null=True)
    phone = models.CharField(max_length=160, blank=True, null=True)
    descrip = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CMIS_UCLAPI_V_BOOKINGS'


class Room(models.Model):
    setid = models.CharField(max_length=40, blank=True, null=True)
    siteid = models.CharField(max_length=40, blank=True, null=True)
    sitename = models.CharField(max_length=320, blank=True, null=True)
    address1 = models.CharField(max_length=320, blank=True, null=True)
    address2 = models.CharField(max_length=320, blank=True, null=True)
    address3 = models.CharField(max_length=320, blank=True, null=True)
    address4 = models.CharField(max_length=320, blank=True, null=True)
    roomid = models.CharField(max_length=40, primary_key=True)
    roomname = models.CharField(max_length=320, blank=True, null=True)
    roomdeptid = models.CharField(max_length=40, blank=True, null=True)
    bookabletype = models.CharField(max_length=40, blank=True, null=True)
    roomclass = models.CharField(max_length=40, blank=True, null=True)
    zone = models.CharField(max_length=40, blank=True, null=True)
    webview = models.CharField(max_length=4, blank=True, null=True)
    automated = models.CharField(max_length=4, blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CMIS_UCLAPI_V_ROOMS'


class Equipment(models.Model):
    setid = models.CharField(max_length=40, blank=True, null=True)
    roomid = models.CharField(max_length=40, primary_key=True)
    units = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=320, blank=True, null=True)
    siteid = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CMIS_UCLAPI_V_EQUIP_FEATURES'


class PageToken(models.Model):
    page_token = models.CharField(
                    max_length=2000,
                    unique=True,
                    default=generate_token)
    pagination = models.IntegerField(default=20)
    query = models.CharField(max_length=100000)
    curr_page = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def get_query(self):
        return json.loads(self.query)

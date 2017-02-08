from __future__ import unicode_literals

from django.db import models
from .api_helpers import generate_token

class Booking(models.Model):
    setid = models.CharField(max_length=40, blank=True, null=True)
    siteid = models.CharField(max_length=40, blank=True, null=True)
    roomid = models.CharField(max_length=40, blank=True, null=True)
    sitename = models.CharField(max_length=320, blank=True, null=True)
    roomname = models.CharField(max_length=320, blank=True, null=True)
    roomdeptid = models.CharField(max_length=40, blank=True, null=True)
    bookabletype = models.CharField(max_length=40, blank=True, null=True)
    roomclass = models.CharField(max_length=40, blank=True, null=True)
    zone = models.CharField(max_length=40, blank=True, null=True)
    webview = models.CharField(max_length=4, blank=True, null=True)
    automated = models.CharField(max_length=4, blank=True, null=True)
    slotid = models.BigIntegerField(primary_key=True)
    bookingid = models.CharField(max_length=80, blank=True, null=True)
    starttime = models.CharField(max_length=20, blank=True, null=True)
    finishtime = models.CharField(max_length=20, blank=True, null=True)
    startdatetime = models.DateField(blank=True, null=True)
    finishdatetime = models.DateField(blank=True, null=True)
    weekday = models.BigIntegerField(blank=True, null=True)
    dayname = models.CharField(max_length=144, blank=True, null=True)
    weekid = models.BigIntegerField(blank=True, null=True)
    weeknumber = models.FloatField(blank=True, null=True)
    mapdate = models.DateField(blank=True, null=True)
    lecturerid = models.CharField(max_length=40, blank=True, null=True)
    lecturername = models.CharField(max_length=4000, blank=True, null=True)
    contactid = models.CharField(max_length=40, blank=True, null=True)
    contactname = models.CharField(max_length=320, blank=True, null=True)
    contype = models.CharField(max_length=40, blank=True, null=True)
    contactused = models.CharField(max_length=32, blank=True, null=True)
    condisplayname = models.CharField(max_length=4000, blank=True, null=True)
    phone = models.CharField(max_length=160, blank=True, null=True)
    exdirectory = models.CharField(max_length=4, blank=True, null=True)
    firstmodid = models.CharField(max_length=48, blank=True, null=True)
    firstmodgrp = models.CharField(max_length=40, blank=True, null=True)
    firstmodname = models.CharField(max_length=480, blank=True, null=True)
    gendatastring = models.CharField(max_length=400, blank=True, null=True)
    descrip = models.CharField(max_length=400, blank=True, null=True)
    title = models.CharField(max_length=532, blank=True, null=True)
    classid = models.CharField(max_length=40, blank=True, null=True)
    eventtype = models.CharField(max_length=220, blank=True, null=True)
    closed = models.CharField(max_length=4, blank=True, null=True)
    status = models.BigIntegerField(blank=True, null=True)
    cancelled = models.CharField(max_length=4, blank=True, null=True)
    provisional = models.CharField(max_length=4, blank=True, null=True)
    modslotentry = models.BigIntegerField(blank=True, null=True)
    moduleid = models.CharField(max_length=48, blank=True, null=True)
    modgrpcode = models.CharField(max_length=40, blank=True, null=True)
    modulename = models.CharField(max_length=480, blank=True, null=True)
    datestring = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CMIS_V_DIARYINFO'


class Room(models.Model):
    roomid = models.CharField(max_length=40, primary_key=True)
    siteid = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=320, blank=True, null=True)
    category = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    classification = models.CharField(max_length=40, blank=True, null=True)
    roomgrpcode = models.CharField(max_length=40, blank=True, null=True)
    zone = models.CharField(max_length=40, blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    prefmin = models.FloatField(blank=True, null=True)
    prefmax = models.FloatField(blank=True, null=True)
    deptid = models.CharField(max_length=40, blank=True, null=True)
    roomarea = models.FloatField(blank=True, null=True)
    dynafill = models.CharField(max_length=4, blank=True, null=True)
    setid = models.CharField(max_length=40, blank=True, null=True)
    uniquefield = models.CharField(max_length=40, blank=True, null=True)
    linkcode = models.CharField(max_length=80, blank=True, null=True)
    campusid = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rooms'


class PageToken(models.Model):
    page_token = models.CharField(
                    max_length=2000,
                    unique=True,
                    default=generate_token)
    pagination = models.IntegerField(default=20)
    query = models.CharField(max_length=100000)
    curr_page = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

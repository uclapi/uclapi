from django.db import models

models.options.DEFAULT_NAMES += ('_DATABASE',)


class Weekstructure(models.Model):
    setid = models.TextField(max_length=10)
    weeknumber = models.BigIntegerField()
    startdate = models.DateField()
    description = models.TextField(primary_key=True, max_length=80)
    mappedto = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_WEEKSTRUCTURE'
        _DATABASE = 'roombookings'


class Students(models.Model):
    setid = models.TextField(max_length=10)
    studentid = models.TextField(primary_key=True, max_length=12)
    name = models.TextField(max_length=120)
    linkcode = models.TextField(max_length=20)
    courseid = models.TextField(max_length=12)
    courseyear = models.BigIntegerField()
    classgroupid = models.TextField(max_length=10)
    deptid = models.TextField(max_length=10)
    instcode = models.TextField(max_length=10)
    qtype1 = models.TextField(max_length=10)
    qtype2 = models.TextField(max_length=10)
    qtype3 = models.TextField(max_length=10)
    regchecked = models.CharField(max_length=1)
    fullypaid = models.CharField(max_length=1)
    house1 = models.BigIntegerField()
    house2 = models.BigIntegerField()
    lecturerid = models.TextField(max_length=10)
    optionblockid = models.BigIntegerField()
    rulesetid = models.TextField(max_length=10)
    semid = models.BigIntegerField()
    instid = models.BigIntegerField()
    isflipflop = models.CharField(max_length=1)
    crsver = models.BigIntegerField()
    finalyear = models.CharField(max_length=1)
    newcourseid = models.TextField(max_length=12)
    lastsemrank = models.BigIntegerField()
    acadstanding = models.BigIntegerField()
    isdeferred = models.CharField(max_length=1)
    oldcourseid = models.TextField(max_length=12)
    oldcourseyear = models.BigIntegerField()
    oldsemid = models.BigIntegerField()
    oldacadstanding = models.BigIntegerField()
    acaddone = models.BigIntegerField()
    semrank = models.BigIntegerField()
    oldsemrank = models.BigIntegerField()
    custate = models.BigIntegerField()
    oldcustate = models.BigIntegerField()
    progstoskip = models.BigIntegerField()
    adjacadstanding = models.BigIntegerField()
    ema = models.CharField(max_length=1)
    emaid = models.TextField(max_length=12)
    dob = models.DateField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_STUDENTS'
        _DATABASE = 'roombookings'


class Sites(models.Model):
    setid = models.TextField(max_length=10)
    siteid = models.TextField(max_length=10)
    sitename = models.TextField(max_length=80)
    address1 = models.TextField(max_length=80)
    address2 = models.TextField(primary_key=True, max_length=80)
    address3 = models.TextField(max_length=80)
    address4 = models.TextField(max_length=80)
    phone1 = models.TextField(max_length=50)
    phone2 = models.TextField(max_length=50)
    contact1 = models.TextField(max_length=50)
    contact2 = models.TextField(max_length=50)
    linkcode = models.TextField(max_length=20)
    campusid = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_SITES'
        _DATABASE = 'roombookings'


class Module(models.Model):
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(primary_key=True, max_length=12)
    owner = models.TextField(max_length=10)
    name = models.TextField(max_length=120)
    category = models.TextField(max_length=10)
    classif = models.TextField(max_length=10)
    linkcode = models.TextField(primary_key=True, max_length=20)
    csize = models.BigIntegerField()
    minsize = models.BigIntegerField()
    maxsize = models.BigIntegerField()
    prefmaxsize = models.BigIntegerField()
    lecturerid = models.TextField(max_length=10)
    lectgroup = models.BigIntegerField()
    dontfit = models.CharField(max_length=1)
    unitvalue = models.TextField(max_length=10)
    instid = models.BigIntegerField()
    isactive = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_MODULE'
        _DATABASE = 'roombookings'


class Lecturer(models.Model):
    setid = models.TextField(max_length=10)
    lecturerid = models.TextField(max_length=10)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10)
    status = models.TextField(max_length=10)
    parttime = models.TextField(max_length=20)
    cost = models.BigIntegerField()
    costtype = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    owner = models.TextField(max_length=10)
    displectid = models.TextField(primary_key=True, max_length=10)
    covprior = models.BigIntegerField()
    covingprior = models.BigIntegerField()
    excludecover = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_LECTURER'
        _DATABASE = 'roombookings'


class Sources(models.Model):
    setid = models.TextField(max_length=10)
    sourcesid = models.TextField(primary_key=True, max_length=20)
    name = models.TextField(max_length=250)
    descrip = models.TextField(max_length=100)
    deptid = models.TextField(max_length=10)
    username = models.TextField(max_length=50)
    priority = models.BigIntegerField()
    addedon = models.TextField(max_length=25)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_SOURCES'
        _DATABASE = 'roombookings'


class Ccalmaps(models.Model):
    setid = models.TextField(primary_key=True, max_length=10)
    dayposn = models.BigIntegerField()
    weeknum = models.BigIntegerField()
    mapdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_CCALMAPS'
        _DATABASE = 'roombookings'


class Depts(models.Model):
    deptid = models.TextField(max_length=10)
    name = models.TextField(max_length=250)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    headofdepartment = models.TextField(primary_key=True, max_length=50)
    headphone = models.TextField(max_length=50)
    address1 = models.TextField(max_length=50)
    address2 = models.TextField(max_length=50)
    address3 = models.TextField(max_length=50)
    address4 = models.TextField(max_length=50)
    admincontact = models.TextField(max_length=50)
    adminphone = models.TextField(max_length=50)
    lecturerid = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_DEPTS'
        _DATABASE = 'roombookings'


class Weekmapstring(models.Model):
    setid = models.TextField(max_length=10)
    weekid = models.BigIntegerField()
    name = models.TextField(max_length=50)
    weeks = models.TextField(max_length=104)
    numweeks = models.BigIntegerField()
    statweeks = models.TextField(primary_key=True, max_length=10)
    drstatus = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_WEEKMAPSTRING'
        _DATABASE = 'roombookings'


class Contact(models.Model):
    setid = models.TextField(max_length=10)
    contactid = models.TextField(primary_key=True, max_length=10)
    name = models.TextField(max_length=80)
    company = models.TextField(max_length=80)
    address = models.TextField(max_length=200)
    phone = models.TextField(max_length=40)
    email = models.TextField(max_length=80)
    linkcode = models.TextField(max_length=20)
    owner = models.TextField(max_length=10)
    concat = models.TextField(max_length=10)
    contype = models.TextField(max_length=10)
    slipbk = models.TextField(max_length=40)
    slipemail = models.TextField(max_length=40)
    faxnumber = models.TextField(max_length=25)
    mobilenumber = models.TextField(max_length=25)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_CONTACT'
        _DATABASE = 'roombookings'


class Slotdetails(models.Model):
    setid = models.TextField(max_length=10)
    slotid = models.BigIntegerField()
    slotline = models.BigIntegerField()
    descrip = models.TextField(max_length=100)
    cost = models.BigIntegerField()
    costdets = models.TextField(max_length=30)
    sourcesid = models.TextField(max_length=20)
    drstatus = models.BigIntegerField()
    contact = models.TextField(max_length=10)
    conorg = models.TextField(max_length=10)
    connotify = models.TextField(max_length=10)
    connotorg = models.TextField(max_length=10)
    pubstart = models.TextField(max_length=5)
    pubfinish = models.TextField(max_length=5)
    datecreated = models.TextField(max_length=12)
    datenotified = models.TextField(max_length=12)
    dateconfirmed = models.TextField(max_length=12)
    reminderdays = models.BigIntegerField()
    bookingid = models.TextField(max_length=20)
    notes = models.TextField(max_length=100)
    speaker = models.TextField(max_length=40)
    spktitle = models.TextField(max_length=40)
    spktopic = models.TextField(primary_key=True, max_length=50)
    spkaddr = models.TextField(max_length=100)
    urlline = models.TextField(max_length=100)
    weeklystatus = models.TextField(max_length=60)
    spkchair = models.TextField(max_length=60)
    bookingstatus = models.TextField(max_length=10)
    sourcecreated = models.BigIntegerField()
    usercreated = models.TextField(max_length=30)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_SLOTDETAILS'
        _DATABASE = 'roombookings'


class Classgrps(models.Model):
    setid = models.TextField(max_length=10)
    classgroupid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    grpcode = models.TextField(max_length=10)
    crsyear = models.BigIntegerField()
    name = models.TextField(max_length=25)
    csize = models.BigIntegerField()
    minsize = models.BigIntegerField()
    maxsize = models.BigIntegerField()
    prefmaxsize = models.BigIntegerField()
    linkcode = models.TextField(primary_key=True, max_length=20)
    estsize = models.BigIntegerField()
    thiskey = models.BigIntegerField()
    parentkey = models.BigIntegerField()
    groupnum = models.BigIntegerField()
    cequivid = models.BigIntegerField()
    year = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_CLASSGRPS'
        _DATABASE = 'roombookings'


class Crscompmodules(models.Model):
    setid = models.TextField(max_length=10)
    courseid = models.TextField(primary_key=True, max_length=12)
    crsyear = models.BigIntegerField()
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    instid = models.BigIntegerField()
    semid = models.BigIntegerField()
    unitvalue = models.TextField(max_length=19)
    crsver = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_CRSCOMPMODULES'
        _DATABASE = 'roombookings'


class Classifications(models.Model):
    setid = models.TextField(max_length=10)
    classid = models.TextField(max_length=10)
    type = models.TextField(max_length=15)
    name = models.TextField(primary_key=True, max_length=55)
    description = models.TextField(max_length=120)
    linkcode = models.TextField(max_length=20)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_CLASSIFICATIONS'
        _DATABASE = 'roombookings'


class Rooms(models.Model):
    roomid = models.TextField(max_length=10)
    siteid = models.TextField(max_length=10)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10)
    classification = models.TextField(primary_key=True, max_length=10)
    roomgrpcode = models.TextField(max_length=10)
    zone = models.TextField(max_length=10)
    capacity = models.BigIntegerField()
    prefmin = models.BigIntegerField()
    prefmax = models.BigIntegerField()
    deptid = models.TextField(max_length=10)
    roomarea = models.BigIntegerField()
    dynafill = models.CharField(max_length=1)
    setid = models.TextField(max_length=10)
    uniquefield = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    campusid = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_ROOMS'
        _DATABASE = 'roombookings'


class Weekmapnumeric(models.Model):
    setid = models.TextField(primary_key=True, max_length=10)
    weekid = models.BigIntegerField()
    weeknumber = models.BigIntegerField()
    drstatus = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_WEEKMAPNUMERIC'
        _DATABASE = 'roombookings'


class Crsavailmodules(models.Model):
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField()
    groupnum = models.BigIntegerField()
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(primary_key=True, max_length=12)
    instid = models.BigIntegerField()
    semid = models.BigIntegerField()
    unitvalue = models.TextField(max_length=19)
    crsver = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_CRSAVAILMODULES'
        _DATABASE = 'roombookings'


class Timetable(models.Model):
    slotid = models.BigIntegerField(primary_key=True)
    slotentry = models.BigIntegerField()
    slottotal = models.BigIntegerField()
    setid = models.TextField(max_length=10)
    periodid = models.BigIntegerField()
    weekday = models.BigIntegerField()
    starttime = models.TextField(max_length=5)
    duration = models.BigIntegerField()
    finishtime = models.TextField(max_length=5)
    weekid = models.BigIntegerField()
    classgroupid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    courseyear = models.BigIntegerField()
    clsgrpcode = models.TextField(max_length=10)
    lecturerid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    deptid = models.TextField(max_length=10)
    moduletype = models.TextField(max_length=10)
    modgrpcode = models.TextField(max_length=10)
    siteid = models.TextField(max_length=10)
    roomid = models.TextField(max_length=10)
    roomgrpcode = models.TextField(max_length=10)
    sourcesid = models.TextField(max_length=20)
    capacity = models.BigIntegerField()
    reqsiteid = models.TextField(max_length=10)
    reqroomid = models.TextField(max_length=10)
    reqtype = models.TextField(max_length=10)
    reqcategory = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=10)
    linkid = models.BigIntegerField()
    chainid = models.BigIntegerField()
    exclid = models.BigIntegerField()
    associd = models.BigIntegerField()
    specid = models.BigIntegerField()
    locked = models.BigIntegerField()
    status = models.BigIntegerField()
    readlock = models.BigIntegerField()
    classif = models.TextField(max_length=10)
    owner = models.TextField(max_length=10)
    drstatus = models.BigIntegerField()
    lectgrp = models.BigIntegerField()
    evpriority = models.BigIntegerField()
    fixlect = models.CharField(max_length=1)
    fixroom = models.CharField(max_length=1)
    fixevent = models.CharField(max_length=1)
    reqclass = models.TextField(max_length=10)
    reqzone = models.TextField(max_length=10)
    tweightid = models.BigIntegerField()
    fixweight = models.BigIntegerField()
    siteproximity = models.BigIntegerField()
    zoneproximity = models.BigIntegerField()
    maxrooms = models.BigIntegerField()
    datechanged = models.TextField(max_length=12)
    sizeused = models.BigIntegerField()
    uniquefield = models.TextField(max_length=10)
    equipid = models.TextField(max_length=10)
    ecode = models.TextField(max_length=20)
    einstalled = models.TextField(max_length=12)
    eremoved = models.TextField(max_length=12)
    ewhoinstalled = models.TextField(max_length=20)
    ewhoremoved = models.TextField(max_length=20)
    tobecopied = models.CharField(max_length=1)
    copied = models.CharField(max_length=1)
    excludefit = models.CharField(max_length=1)
    gendatanum = models.BigIntegerField()
    gendatastring = models.TextField(max_length=100)
    regid = models.BigIntegerField()
    sourcechange = models.BigIntegerField()
    userchange = models.TextField(max_length=30)
    mequipcat = models.TextField(max_length=10)
    mequiptype = models.TextField(max_length=10)
    mequipnotes = models.CharField(max_length=1)
    triggerdate = models.TextField(max_length=10)
    reqcampusid = models.TextField(max_length=10)
    instid = models.BigIntegerField()
    numperiods = models.BigIntegerField()
    maxperiodgap = models.BigIntegerField()
    groupid = models.BigIntegerField()
    tobescheduled = models.BigIntegerField()
    board = models.TextField(max_length=10)
    series = models.TextField(max_length=10)
    crsyear = models.TextField(max_length=4)
    optcode = models.TextField(max_length=10)
    compcode = models.TextField(max_length=20)
    subcode = models.TextField(max_length=10)
    compinstid = models.BigIntegerField()
    roompoolid = models.BigIntegerField()
    nonconid = models.BigIntegerField()
    typeevent = models.BigIntegerField()
    ncyear = models.TextField(max_length=3)
    reasonforchange = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = "NOSH_CMIS_TIMETABLE"
        _DATABASE = 'roombookings'


class Stumodules(models.Model):
    setid = models.TextField(max_length=10)
    studentid = models.TextField(primary_key=True, max_length=12)
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    modgrpcode = models.TextField(max_length=10)
    slotid = models.BigIntegerField()
    fixingrp = models.CharField(max_length=1)
    modpart = models.TextField(max_length=10)
    restype = models.TextField(max_length=10)
    unitvalue = models.TextField(max_length=10)
    classif = models.TextField(max_length=10)
    papernum = models.BigIntegerField()
    modlevel = models.TextField(max_length=10)
    inactive = models.CharField(max_length=1)
    instid = models.BigIntegerField()
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField()
    semid = models.BigIntegerField()
    moddropped = models.CharField(max_length=1)
    donotcount = models.CharField(max_length=1)
    semrank = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_STUMODULES'
        _DATABASE = 'roombookings'


class Features(models.Model):
    setid = models.TextField(max_length=10)
    featureid = models.TextField(max_length=10)
    description = models.TextField(primary_key=True, max_length=80)
    linkcode = models.TextField(max_length=20)
    contactid = models.TextField(max_length=10)
    cost = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_FEATURES'
        _DATABASE = 'roombookings'


class Equipment(models.Model):
    setid = models.TextField(max_length=10)
    equipid = models.TextField(primary_key=True, max_length=10)
    description = models.TextField(max_length=80)
    linkcode = models.TextField(max_length=20)
    contactid = models.TextField(max_length=10)
    cost = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_EQUIPMENT'
        _DATABASE = 'roombookings'


class Course(models.Model):
    setid = models.TextField(max_length=10)
    courseid = models.TextField(primary_key=True, max_length=12)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    owner = models.TextField(max_length=10)
    numyears = models.BigIntegerField()
    crsweight = models.FloatField()
    minmodules = models.BigIntegerField()
    maxmodules = models.BigIntegerField()
    numplaces = models.BigIntegerField()
    mintotal = models.BigIntegerField()
    maxtotal = models.BigIntegerField()
    firstyear = models.BigIntegerField()
    oldcourseid = models.TextField(max_length=12)
    isactive = models.CharField(max_length=1)
    lecturerid = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = 'NOSH_CMIS_COURSE'
        _DATABASE = 'roombookings'

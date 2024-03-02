from django.db import models

models.options.DEFAULT_NAMES += ('_DATABASE',)


class Weekstructure(models.Model):
    setid = models.TextField(max_length=10)
    weeknumber = models.BigIntegerField(null=True, blank=True)
    startdate = models.DateField(primary_key=True)
    description = models.TextField(null=True, max_length=80)
    mappedto = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."WEEKSTRUCTURE"'
        _DATABASE = 'roombookings'


class WeekstructureA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    weeknumber = models.BigIntegerField(null=True, blank=True)
    startdate = models.DateField()
    description = models.TextField(max_length=80, null=True)
    mappedto = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class WeekstructureB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    weeknumber = models.BigIntegerField(null=True, blank=True)
    startdate = models.DateField()
    description = models.TextField(max_length=80, null=True)
    mappedto = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Students(models.Model):
    setid = models.TextField(max_length=10)
    studentid = models.TextField(primary_key=True, max_length=12)
    name = models.TextField(max_length=120)
    linkcode = models.TextField(max_length=20, null=True)
    courseid = models.TextField(max_length=12, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    classgroupid = models.TextField(max_length=10, null=True)
    deptid = models.TextField(max_length=10)
    instcode = models.TextField(max_length=10)
    qtype1 = models.TextField(max_length=10)
    qtype2 = models.TextField(max_length=10)
    qtype3 = models.TextField(max_length=10, null=True)
    regchecked = models.CharField(max_length=1, null=True)
    fullypaid = models.CharField(max_length=1, null=True)
    house1 = models.BigIntegerField(null=True, blank=True)
    house2 = models.BigIntegerField(null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True)
    optionblockid = models.BigIntegerField(null=True, blank=True)
    rulesetid = models.TextField(max_length=10, null=True)
    semid = models.BigIntegerField(null=True, blank=True)
    instid = models.BigIntegerField(null=True, blank=True)
    isflipflop = models.CharField(max_length=1, null=True)
    crsver = models.BigIntegerField(null=True, blank=True)
    finalyear = models.CharField(max_length=1, null=True)
    newcourseid = models.TextField(max_length=12, null=True)
    lastsemrank = models.BigIntegerField(null=True, blank=True)
    acadstanding = models.BigIntegerField(null=True, blank=True)
    isdeferred = models.CharField(max_length=1, null=True)
    oldcourseid = models.TextField(max_length=12, null=True)
    oldcourseyear = models.BigIntegerField(null=True, blank=True)
    oldsemid = models.BigIntegerField(null=True, blank=True)
    oldacadstanding = models.BigIntegerField(null=True, blank=True)
    acaddone = models.BigIntegerField(null=True, blank=True)
    semrank = models.BigIntegerField(null=True, blank=True)
    oldsemrank = models.BigIntegerField(null=True, blank=True)
    custate = models.BigIntegerField(null=True, blank=True)
    oldcustate = models.BigIntegerField(null=True, blank=True)
    progstoskip = models.BigIntegerField(null=True, blank=True)
    adjacadstanding = models.BigIntegerField(null=True, blank=True)
    ema = models.CharField(max_length=1, null=True)
    emaid = models.TextField(max_length=12, null=True)
    dob = models.DateField(null=True)
    field1 = models.CharField(max_length=55, null=True)
    field2 = models.CharField(max_length=55, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."STUDENTS"'
        _DATABASE = 'roombookings'


class StudentsA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    studentid = models.TextField(max_length=12)
    name = models.TextField(max_length=120)
    linkcode = models.TextField(max_length=20, null=True)
    courseid = models.TextField(max_length=12, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    classgroupid = models.TextField(max_length=10, null=True)
    deptid = models.TextField(max_length=10)
    instcode = models.TextField(max_length=10)
    qtype1 = models.TextField(max_length=10)
    qtype2 = models.TextField(max_length=10)
    qtype3 = models.TextField(max_length=10, null=True)
    regchecked = models.CharField(max_length=1, null=True)
    fullypaid = models.CharField(max_length=1, null=True)
    house1 = models.BigIntegerField(null=True, blank=True)
    house2 = models.BigIntegerField(null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True)
    optionblockid = models.BigIntegerField(null=True, blank=True)
    rulesetid = models.TextField(max_length=10, null=True)
    semid = models.BigIntegerField(null=True, blank=True)
    instid = models.BigIntegerField(null=True, blank=True)
    isflipflop = models.CharField(max_length=1, null=True)
    crsver = models.BigIntegerField(null=True, blank=True)
    finalyear = models.CharField(max_length=1, null=True)
    newcourseid = models.TextField(max_length=12, null=True)
    lastsemrank = models.BigIntegerField(null=True, blank=True)
    acadstanding = models.BigIntegerField(null=True, blank=True)
    isdeferred = models.CharField(max_length=1, null=True)
    oldcourseid = models.TextField(max_length=12, null=True)
    oldcourseyear = models.BigIntegerField(null=True, blank=True)
    oldsemid = models.BigIntegerField(null=True, blank=True)
    oldacadstanding = models.BigIntegerField(null=True, blank=True)
    acaddone = models.BigIntegerField(null=True, blank=True)
    semrank = models.BigIntegerField(null=True, blank=True)
    oldsemrank = models.BigIntegerField(null=True, blank=True)
    custate = models.BigIntegerField(null=True, blank=True)
    oldcustate = models.BigIntegerField(null=True, blank=True)
    progstoskip = models.BigIntegerField(null=True, blank=True)
    adjacadstanding = models.BigIntegerField(null=True, blank=True)
    ema = models.CharField(max_length=1, null=True)
    emaid = models.TextField(max_length=12, null=True)
    dob = models.DateField(null=True, blank=True)
    field1 = models.CharField(max_length=55, null=True)
    field2 = models.CharField(max_length=55, null=True)

    class Meta:
        _DATABASE = 'gencache'


class StudentsB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    studentid = models.TextField(max_length=12)
    name = models.TextField(max_length=120)
    linkcode = models.TextField(max_length=20, null=True)
    courseid = models.TextField(max_length=12, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    classgroupid = models.TextField(max_length=10, null=True)
    deptid = models.TextField(max_length=10)
    instcode = models.TextField(max_length=10)
    qtype1 = models.TextField(max_length=10)
    qtype2 = models.TextField(max_length=10)
    qtype3 = models.TextField(max_length=10, null=True)
    regchecked = models.CharField(max_length=1, null=True)
    fullypaid = models.CharField(max_length=1, null=True)
    house1 = models.BigIntegerField(null=True, blank=True)
    house2 = models.BigIntegerField(null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True)
    optionblockid = models.BigIntegerField(null=True, blank=True)
    rulesetid = models.TextField(max_length=10, null=True)
    semid = models.BigIntegerField(null=True, blank=True)
    instid = models.BigIntegerField(null=True, blank=True)
    isflipflop = models.CharField(max_length=1, null=True)
    crsver = models.BigIntegerField(null=True, blank=True)
    finalyear = models.CharField(max_length=1, null=True)
    newcourseid = models.TextField(max_length=12, null=True)
    lastsemrank = models.BigIntegerField(null=True, blank=True)
    acadstanding = models.BigIntegerField(null=True, blank=True)
    isdeferred = models.CharField(max_length=1, null=True)
    oldcourseid = models.TextField(max_length=12, null=True)
    oldcourseyear = models.BigIntegerField(null=True, blank=True)
    oldsemid = models.BigIntegerField(null=True, blank=True)
    oldacadstanding = models.BigIntegerField(null=True, blank=True)
    acaddone = models.BigIntegerField(null=True, blank=True)
    semrank = models.BigIntegerField(null=True, blank=True)
    oldsemrank = models.BigIntegerField(null=True, blank=True)
    custate = models.BigIntegerField(null=True, blank=True)
    oldcustate = models.BigIntegerField(null=True, blank=True)
    progstoskip = models.BigIntegerField(null=True, blank=True)
    adjacadstanding = models.BigIntegerField(null=True, blank=True)
    ema = models.CharField(max_length=1, null=True)
    emaid = models.TextField(max_length=12, null=True)
    dob = models.DateField(null=True, blank=True)
    field1 = models.CharField(max_length=55, null=True)
    field2 = models.CharField(max_length=55, null=True)

    class Meta:
        _DATABASE = 'gencache'


class Sites(models.Model):
    setid = models.TextField(max_length=10)
    siteid = models.TextField(primary_key=True, max_length=10)
    sitename = models.TextField(max_length=80)
    address1 = models.TextField(max_length=80, null=True)
    address2 = models.TextField(max_length=80, null=True)
    address3 = models.TextField(max_length=80, null=True)
    address4 = models.TextField(max_length=80, null=True)
    phone1 = models.TextField(max_length=50, null=True)
    phone2 = models.TextField(max_length=50, null=True)
    contact1 = models.TextField(max_length=50, null=True)
    contact2 = models.TextField(max_length=50, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    campusid = models.TextField(max_length=10, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."SITES"'
        _DATABASE = 'roombookings'


class SitesA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    siteid = models.TextField(max_length=10)
    sitename = models.TextField(max_length=80)
    address1 = models.TextField(max_length=80, null=True)
    address2 = models.TextField(max_length=80, null=True)
    address3 = models.TextField(max_length=80, null=True)
    address4 = models.TextField(max_length=80, null=True)
    phone1 = models.TextField(max_length=50, null=True)
    phone2 = models.TextField(max_length=50, null=True)
    contact1 = models.TextField(max_length=50, null=True)
    contact2 = models.TextField(max_length=50, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    campusid = models.TextField(max_length=10, null=True)

    class Meta:
        _DATABASE = 'gencache'


class SitesB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    siteid = models.TextField(max_length=10)
    sitename = models.TextField(max_length=80)
    address1 = models.TextField(max_length=80, null=True)
    address2 = models.TextField(max_length=80, null=True)
    address3 = models.TextField(max_length=80, null=True)
    address4 = models.TextField(max_length=80, null=True)
    phone1 = models.TextField(max_length=50, null=True)
    phone2 = models.TextField(max_length=50, null=True)
    contact1 = models.TextField(max_length=50, null=True)
    contact2 = models.TextField(max_length=50, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    campusid = models.TextField(max_length=10, null=True)

    class Meta:
        _DATABASE = 'gencache'


class Module(models.Model):
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(primary_key=True, max_length=12)
    owner = models.TextField(max_length=10)
    name = models.TextField(max_length=120)
    category = models.TextField(max_length=10, null=True)
    classif = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    csize = models.BigIntegerField(null=True, blank=True)
    minsize = models.BigIntegerField(null=True, blank=True)
    maxsize = models.BigIntegerField(null=True, blank=True)
    prefmaxsize = models.BigIntegerField(null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True)
    lectgroup = models.BigIntegerField(null=True, blank=True)
    dontfit = models.CharField(max_length=1, null=True)
    unitvalue = models.TextField(max_length=10, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    isactive = models.CharField(max_length=1, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."MODULE"'
        _DATABASE = 'roombookings'
        unique_together = (("linkcode", "moduleid"),)


class ModuleA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    owner = models.TextField(max_length=10)
    name = models.TextField(max_length=120)
    category = models.TextField(max_length=10, null=True)
    classif = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    csize = models.BigIntegerField(null=True, blank=True)
    minsize = models.BigIntegerField(null=True, blank=True)
    maxsize = models.BigIntegerField(null=True, blank=True)
    prefmaxsize = models.BigIntegerField(null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True)
    lectgroup = models.BigIntegerField(null=True, blank=True)
    dontfit = models.CharField(max_length=1, null=True)
    unitvalue = models.TextField(max_length=10)
    instid = models.BigIntegerField(null=True, blank=True)
    isactive = models.CharField(max_length=1, null=True)

    class Meta:
        _DATABASE = 'gencache'


class ModuleB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    owner = models.TextField(max_length=10)
    name = models.TextField(max_length=120)
    category = models.TextField(max_length=10, null=True)
    classif = models.TextField(max_length=10)
    linkcode = models.TextField(max_length=20)
    csize = models.BigIntegerField(null=True, blank=True)
    minsize = models.BigIntegerField(null=True, blank=True)
    maxsize = models.BigIntegerField(null=True, blank=True)
    prefmaxsize = models.BigIntegerField(null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True)
    lectgroup = models.BigIntegerField(null=True, blank=True)
    dontfit = models.CharField(max_length=1, null=True)
    unitvalue = models.TextField(max_length=10)
    instid = models.BigIntegerField(null=True, blank=True)
    isactive = models.CharField(max_length=1, null=True)

    class Meta:
        _DATABASE = 'gencache'


class Lecturer(models.Model):
    setid = models.TextField(max_length=10)
    lecturerid = models.TextField(max_length=10)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10, null=True)
    type = models.TextField(max_length=10, null=True)
    status = models.TextField(max_length=10)
    parttime = models.TextField(max_length=20, null=True)
    cost = models.BigIntegerField(null=True, blank=True)
    costtype = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    owner = models.TextField(max_length=10)
    displectid = models.TextField(primary_key=True, max_length=10)
    covprior = models.BigIntegerField(null=True, blank=True)
    covingprior = models.BigIntegerField(null=True, blank=True)
    excludecover = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."LECTURER"'
        _DATABASE = 'roombookings'


class LecturerA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    lecturerid = models.TextField(max_length=10, null=True, blank=True)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10, null=True, blank=True)
    type = models.TextField(max_length=10, null=True, blank=True)
    status = models.TextField(max_length=10, null=True, blank=True)
    parttime = models.TextField(max_length=20, null=True, blank=True)
    cost = models.BigIntegerField(null=True, blank=True)
    costtype = models.TextField(max_length=10, null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    owner = models.TextField(max_length=10)
    displectid = models.TextField(max_length=10)
    covprior = models.BigIntegerField(null=True, blank=True)
    covingprior = models.BigIntegerField(null=True, blank=True)
    excludecover = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class LecturerB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    lecturerid = models.TextField(max_length=10)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10, null=True, blank=True)
    type = models.TextField(max_length=10, null=True, blank=True)
    status = models.TextField(max_length=10, null=True, blank=True)
    parttime = models.TextField(max_length=20, null=True, blank=True)
    cost = models.BigIntegerField(null=True, blank=True)
    costtype = models.TextField(max_length=10, null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    owner = models.TextField(max_length=10)
    displectid = models.TextField(max_length=10)
    covprior = models.BigIntegerField(null=True, blank=True)
    covingprior = models.BigIntegerField(null=True, blank=True)
    excludecover = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Sources(models.Model):
    setid = models.TextField(max_length=10)
    sourcesid = models.TextField(primary_key=True, max_length=20)
    name = models.TextField(max_length=250)
    descrip = models.TextField(max_length=100)
    deptid = models.TextField(max_length=10, null=True)
    username = models.TextField(max_length=50)
    priority = models.BigIntegerField(null=True, blank=True)
    addedon = models.TextField(max_length=25)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."SOURCES"'
        _DATABASE = 'roombookings'


class Ccalmaps(models.Model):
    setid = models.TextField(primary_key=True, max_length=10)
    dayposn = models.BigIntegerField(null=True, blank=True)
    weeknum = models.BigIntegerField(null=True, blank=True)
    mapdate = models.DateField()

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."CCALMAPS"'
        _DATABASE = 'roombookings'


class Depts(models.Model):
    deptid = models.TextField(primary_key=True, max_length=10)
    name = models.TextField(max_length=250)
    category = models.TextField(max_length=10, null=True)
    type = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    headofdepartment = models.TextField(max_length=50, null=True)
    headphone = models.TextField(max_length=50, null=True)
    address1 = models.TextField(max_length=50, null=True)
    address2 = models.TextField(max_length=50, null=True)
    address3 = models.TextField(max_length=50, null=True)
    address4 = models.TextField(max_length=50, null=True)
    admincontact = models.TextField(max_length=50, null=True)
    adminphone = models.TextField(max_length=50, null=True)
    lecturerid = models.TextField(max_length=10, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."DEPTS"'
        _DATABASE = 'roombookings'


class DeptsA(models.Model):
    id = models.AutoField(primary_key=True)
    deptid = models.TextField(max_length=10)
    name = models.TextField(max_length=250, null=True)
    category = models.TextField(max_length=10, null=True)
    type = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    headofdepartment = models.TextField(max_length=50, null=True)
    headphone = models.TextField(max_length=50, null=True)
    address1 = models.TextField(max_length=50, null=True)
    address2 = models.TextField(max_length=50, null=True)
    address3 = models.TextField(max_length=50, null=True)
    address4 = models.TextField(max_length=50, null=True)
    admincontact = models.TextField(max_length=50, null=True)
    adminphone = models.TextField(max_length=50, null=True)
    lecturerid = models.TextField(max_length=10, null=True)

    class Meta:
        _DATABASE = 'gencache'


class DeptsB(models.Model):
    id = models.AutoField(primary_key=True)
    deptid = models.TextField(max_length=10)
    name = models.TextField(max_length=250, null=True)
    category = models.TextField(max_length=10, null=True)
    type = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20, null=True)
    headofdepartment = models.TextField(max_length=50, null=True)
    headphone = models.TextField(max_length=50, null=True)
    address1 = models.TextField(max_length=50, null=True)
    address2 = models.TextField(max_length=50, null=True)
    address3 = models.TextField(max_length=50, null=True)
    address4 = models.TextField(max_length=50, null=True)
    admincontact = models.TextField(max_length=50, null=True)
    adminphone = models.TextField(max_length=50, null=True)
    lecturerid = models.TextField(max_length=10, null=True)

    class Meta:
        _DATABASE = 'gencache'


class Weekmapstring(models.Model):
    setid = models.TextField(max_length=10)
    weekid = models.BigIntegerField(primary_key=True)
    name = models.TextField(max_length=50, null=True)
    weeks = models.TextField(max_length=104)
    numweeks = models.BigIntegerField(null=True, blank=True)
    statweeks = models.TextField(max_length=10, null=True)
    drstatus = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."WEEKMAPSTRING"'
        _DATABASE = 'roombookings'


class WeekmapstringA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    weekid = models.BigIntegerField(null=True, blank=True)
    name = models.TextField(max_length=50, null=True)
    weeks = models.TextField(max_length=104)
    numweeks = models.BigIntegerField(null=True, blank=True)
    statweeks = models.TextField(max_length=10, null=True)
    drstatus = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class WeekmapstringB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    weekid = models.BigIntegerField(null=True, blank=True)
    name = models.TextField(max_length=50, null=True)
    weeks = models.TextField(max_length=104)
    numweeks = models.BigIntegerField(null=True, blank=True)
    statweeks = models.TextField(max_length=10, null=True)
    drstatus = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


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
        db_table = '"CMIS_OWNER"."CONTACT"'
        _DATABASE = 'roombookings'


class Slotdetails(models.Model):
    setid = models.TextField(max_length=10)
    slotid = models.BigIntegerField(null=True, blank=True)
    slotline = models.BigIntegerField(null=True, blank=True)
    descrip = models.TextField(max_length=100)
    cost = models.BigIntegerField(null=True, blank=True)
    costdets = models.TextField(max_length=30)
    sourcesid = models.TextField(max_length=20)
    drstatus = models.BigIntegerField(null=True, blank=True)
    contact = models.TextField(max_length=10)
    conorg = models.TextField(max_length=10)
    connotify = models.TextField(max_length=10)
    connotorg = models.TextField(max_length=10)
    pubstart = models.TextField(max_length=5)
    pubfinish = models.TextField(max_length=5)
    datecreated = models.TextField(max_length=12)
    datenotified = models.TextField(max_length=12)
    dateconfirmed = models.TextField(max_length=12)
    reminderdays = models.BigIntegerField(null=True, blank=True)
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
    sourcecreated = models.BigIntegerField(null=True, blank=True)
    usercreated = models.TextField(max_length=30)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."SLOTDETAILS"'
        _DATABASE = 'roombookings'


class Classgrps(models.Model):
    setid = models.TextField(max_length=10)
    classgroupid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    grpcode = models.TextField(max_length=10)
    crsyear = models.BigIntegerField(null=True, blank=True)
    name = models.TextField(max_length=25)
    csize = models.BigIntegerField(null=True, blank=True)
    minsize = models.BigIntegerField(null=True, blank=True)
    maxsize = models.BigIntegerField(null=True, blank=True)
    prefmaxsize = models.BigIntegerField(null=True, blank=True)
    linkcode = models.TextField(primary_key=True, max_length=20)
    estsize = models.BigIntegerField(null=True, blank=True)
    thiskey = models.BigIntegerField(null=True, blank=True)
    parentkey = models.BigIntegerField(null=True, blank=True)
    groupnum = models.BigIntegerField(null=True, blank=True)
    cequivid = models.BigIntegerField(null=True, blank=True)
    year = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."CLASSGRPS"'
        _DATABASE = 'roombookings'


class Crscompmodules(models.Model):
    setid = models.TextField(max_length=10)
    courseid = models.TextField(primary_key=True, max_length=12)
    crsyear = models.BigIntegerField(null=True, blank=True)
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    instid = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    unitvalue = models.TextField(max_length=19)
    crsver = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."CRSCOMPMODULES"'
        _DATABASE = 'roombookings'


class CrscompmodulesA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField(null=True, blank=True)
    deptid = models.TextField(max_length=10, blank=True, null=True)
    moduleid = models.TextField(max_length=12)
    instid = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    unitvalue = models.TextField(max_length=19, null=True, blank=True)
    crsver = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class CrscompmodulesB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField(null=True, blank=True)
    deptid = models.TextField(max_length=10, blank=True, null=True)
    moduleid = models.TextField(max_length=12)
    instid = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    unitvalue = models.TextField(max_length=19, null=True, blank=True)
    crsver = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Classifications(models.Model):
    setid = models.CharField(max_length=10, null=True)
    classid = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)
    name = models.CharField(primary_key=True, max_length=55)
    description = models.CharField(max_length=120, null=True)
    linkcode = models.CharField(max_length=20, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."CLASSIFICATIONS"'
        _DATABASE = 'roombookings'


class ClassificationsA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.CharField(max_length=10, null=True)
    classid = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)
    name = models.CharField(max_length=55, null=True)
    description = models.CharField(max_length=120, null=True)
    linkcode = models.CharField(max_length=20, null=True)

    class Meta:
        _DATABASE = 'gencache'


class ClassificationsB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.CharField(max_length=10, null=True)
    classid = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=15, null=True)
    name = models.CharField(max_length=55, null=True)
    description = models.CharField(max_length=120, null=True)
    linkcode = models.CharField(max_length=20, null=True)

    class Meta:
        _DATABASE = 'gencache'


class Weekmapnumeric(models.Model):
    setid = models.TextField(primary_key=True, max_length=10)
    weekid = models.BigIntegerField(null=True, blank=True)
    weeknumber = models.BigIntegerField(null=True, blank=True)
    drstatus = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."WEEKMAPNUMERIC"'
        _DATABASE = 'roombookings'


class WeekmapnumericA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    weekid = models.BigIntegerField(null=True, blank=True)
    weeknumber = models.BigIntegerField(null=True, blank=True)
    drstatus = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class WeekmapnumericB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    weekid = models.BigIntegerField(null=True, blank=True)
    weeknumber = models.BigIntegerField(null=True, blank=True)
    drstatus = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Crsavailmodules(models.Model):
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField(null=True, blank=True)
    groupnum = models.BigIntegerField(null=True, blank=True)
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(primary_key=True, max_length=12)
    instid = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    unitvalue = models.TextField(max_length=19)
    crsver = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."CRSAVAILMODULES"'
        _DATABASE = 'roombookings'


class CrsavailmodulesA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField(null=True, blank=True)
    groupnum = models.BigIntegerField(null=True, blank=True)
    deptid = models.TextField(max_length=10, blank=True, null=True)
    moduleid = models.TextField(max_length=12)
    instid = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    unitvalue = models.TextField(max_length=19, null=True, blank=True)
    crsver = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class CrsavailmodulesB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    crsyear = models.BigIntegerField(null=True, blank=True)
    groupnum = models.BigIntegerField(null=True, blank=True)
    deptid = models.TextField(max_length=10, blank=True, null=True)
    moduleid = models.TextField(max_length=12)
    instid = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    unitvalue = models.TextField(max_length=19, null=True, blank=True)
    crsver = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Timetable(models.Model):
    slotid = models.BigIntegerField(primary_key=True)
    slotentry = models.BigIntegerField(null=True, blank=True)
    slottotal = models.BigIntegerField(null=True, blank=True)
    setid = models.TextField(max_length=10)
    periodid = models.BigIntegerField(null=True, blank=True)
    weekday = models.BigIntegerField(null=True, blank=True)
    starttime = models.TextField(max_length=5, null=True)
    duration = models.BigIntegerField(null=True, blank=True)
    finishtime = models.TextField(max_length=5, null=True)
    weekid = models.BigIntegerField(null=True, blank=True)
    classgroupid = models.TextField(max_length=10, null=True)
    courseid = models.TextField(max_length=12, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    clsgrpcode = models.TextField(max_length=10, null=True)
    lecturerid = models.TextField(max_length=10, null=True)
    moduleid = models.TextField(max_length=12, null=True)
    deptid = models.TextField(max_length=10, null=True)
    moduletype = models.TextField(max_length=10, null=True)
    modgrpcode = models.TextField(max_length=10, null=True)
    siteid = models.TextField(max_length=10, null=True)
    roomid = models.TextField(max_length=10, null=True)
    roomgrpcode = models.TextField(max_length=10, null=True)
    sourcesid = models.TextField(max_length=20)
    capacity = models.BigIntegerField(null=True, blank=True)
    reqsiteid = models.TextField(max_length=10, null=True)
    reqroomid = models.TextField(max_length=10, null=True)
    reqtype = models.TextField(max_length=10, null=True)
    reqcategory = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=10, null=True)
    linkid = models.BigIntegerField(null=True, blank=True)
    chainid = models.BigIntegerField(null=True, blank=True)
    exclid = models.BigIntegerField(null=True, blank=True)
    associd = models.BigIntegerField(null=True, blank=True)
    specid = models.BigIntegerField(null=True, blank=True)
    locked = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    readlock = models.BigIntegerField(null=True, blank=True)
    classif = models.TextField(max_length=10, null=True)
    owner = models.TextField(max_length=10, null=True)
    drstatus = models.BigIntegerField(null=True, blank=True)
    lectgrp = models.BigIntegerField(null=True, blank=True)
    evpriority = models.BigIntegerField(null=True, blank=True)
    fixlect = models.CharField(max_length=1, null=True)
    fixroom = models.CharField(max_length=1, null=True)
    fixevent = models.CharField(max_length=1)
    reqclass = models.TextField(max_length=10, null=True)
    reqzone = models.TextField(max_length=10, null=True)
    tweightid = models.BigIntegerField(null=True, blank=True)
    fixweight = models.BigIntegerField(null=True, blank=True)
    siteproximity = models.BigIntegerField(null=True, blank=True)
    zoneproximity = models.BigIntegerField(null=True, blank=True)
    maxrooms = models.BigIntegerField(null=True, blank=True)
    datechanged = models.TextField(max_length=12, null=True)
    sizeused = models.BigIntegerField(null=True, blank=True)
    uniquefield = models.TextField(max_length=10, null=True)
    equipid = models.TextField(max_length=10, null=True)
    ecode = models.TextField(max_length=20, null=True)
    einstalled = models.TextField(max_length=12, null=True)
    eremoved = models.TextField(max_length=12, null=True)
    ewhoinstalled = models.TextField(max_length=20, null=True)
    ewhoremoved = models.TextField(max_length=20, null=True)
    tobecopied = models.CharField(max_length=1, null=True)
    copied = models.CharField(max_length=1, null=True)
    excludefit = models.CharField(max_length=1, null=True)
    gendatanum = models.BigIntegerField(null=True, blank=True)
    gendatastring = models.TextField(max_length=100, null=True)
    regid = models.BigIntegerField(null=True, blank=True)
    sourcechange = models.BigIntegerField(null=True, blank=True)
    userchange = models.TextField(max_length=30, null=True)
    mequipcat = models.TextField(max_length=10, null=True)
    mequiptype = models.TextField(max_length=10, null=True)
    mequipnotes = models.CharField(max_length=1)
    triggerdate = models.TextField(max_length=10, null=True)
    reqcampusid = models.TextField(max_length=10, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    numperiods = models.BigIntegerField(null=True, blank=True)
    maxperiodgap = models.BigIntegerField(null=True, blank=True)
    groupid = models.BigIntegerField(null=True, blank=True)
    tobescheduled = models.BigIntegerField(null=True, blank=True)
    board = models.TextField(max_length=10, null=True)
    series = models.TextField(max_length=10, null=True)
    crsyear = models.TextField(max_length=4, null=True)
    optcode = models.TextField(max_length=10, null=True)
    compcode = models.TextField(max_length=20, null=True)
    subcode = models.TextField(max_length=10, null=True)
    compinstid = models.BigIntegerField(null=True, blank=True)
    roompoolid = models.BigIntegerField(null=True, blank=True)
    nonconid = models.BigIntegerField(null=True, blank=True)
    typeevent = models.BigIntegerField(null=True, blank=True)
    ncyear = models.TextField(max_length=3, null=True)
    reasonforchange = models.TextField(max_length=10, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."TIMETABLE"'
        _DATABASE = 'roombookings'


class TimetableA(models.Model):
    id = models.AutoField(primary_key=True)
    slotid = models.BigIntegerField(null=True, blank=True)
    slotentry = models.BigIntegerField(null=True, blank=True)
    slottotal = models.BigIntegerField(null=True, blank=True)
    setid = models.TextField(max_length=10)
    periodid = models.BigIntegerField(null=True, blank=True)
    weekday = models.BigIntegerField(null=True, blank=True)
    starttime = models.TextField(max_length=5, null=True)
    duration = models.BigIntegerField(null=True, blank=True)
    finishtime = models.TextField(max_length=5, null=True)
    weekid = models.BigIntegerField(null=True, blank=True)
    classgroupid = models.TextField(max_length=10, null=True)
    courseid = models.TextField(max_length=12, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    clsgrpcode = models.TextField(max_length=10, null=True)
    lecturerid = models.TextField(max_length=10, null=True)
    moduleid = models.TextField(max_length=12, null=True)
    deptid = models.TextField(max_length=10, null=True)
    moduletype = models.TextField(max_length=10, null=True)
    modgrpcode = models.TextField(max_length=10, null=True)
    siteid = models.TextField(max_length=10, null=True)
    roomid = models.TextField(max_length=10, null=True)
    roomgrpcode = models.TextField(max_length=10, null=True)
    sourcesid = models.TextField(max_length=20, null=True)
    capacity = models.BigIntegerField(null=True, blank=True)
    reqsiteid = models.TextField(max_length=10, null=True)
    reqroomid = models.TextField(max_length=10, null=True)
    reqtype = models.TextField(max_length=10, null=True)
    reqcategory = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=10, null=True)
    linkid = models.BigIntegerField(null=True, blank=True)
    chainid = models.BigIntegerField(null=True, blank=True)
    exclid = models.BigIntegerField(null=True, blank=True)
    associd = models.BigIntegerField(null=True, blank=True)
    specid = models.BigIntegerField(null=True, blank=True)
    locked = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    readlock = models.BigIntegerField(null=True, blank=True)
    classif = models.TextField(max_length=10, null=True)
    owner = models.TextField(max_length=10, null=True)
    drstatus = models.BigIntegerField(null=True, blank=True)
    lectgrp = models.BigIntegerField(null=True, blank=True)
    evpriority = models.BigIntegerField(null=True, blank=True)
    fixlect = models.CharField(max_length=1, null=True)
    fixroom = models.CharField(max_length=1, null=True)
    fixevent = models.CharField(max_length=1)
    reqclass = models.TextField(max_length=10, null=True)
    reqzone = models.TextField(max_length=10, null=True)
    tweightid = models.BigIntegerField(null=True, blank=True)
    fixweight = models.BigIntegerField(null=True, blank=True)
    siteproximity = models.BigIntegerField(null=True, blank=True)
    zoneproximity = models.BigIntegerField(null=True, blank=True)
    maxrooms = models.BigIntegerField(null=True, blank=True)
    datechanged = models.TextField(max_length=12, null=True)
    sizeused = models.BigIntegerField(null=True, blank=True)
    # uniquefield has null values in, so we have to account for this
    uniquefield = models.TextField(max_length=10, null=True)
    equipid = models.TextField(max_length=10, null=True)
    ecode = models.TextField(max_length=20, null=True)
    einstalled = models.TextField(max_length=12, null=True)
    eremoved = models.TextField(max_length=12, null=True)
    ewhoinstalled = models.TextField(max_length=20, null=True)
    ewhoremoved = models.TextField(max_length=20, null=True)
    tobecopied = models.CharField(max_length=1, null=True)
    copied = models.CharField(max_length=1, null=True)
    excludefit = models.CharField(max_length=1, null=True)
    gendatanum = models.BigIntegerField(null=True, blank=True)
    gendatastring = models.TextField(max_length=100, null=True)
    regid = models.BigIntegerField(null=True, blank=True)
    sourcechange = models.BigIntegerField(null=True, blank=True)
    userchange = models.TextField(max_length=30, null=True)
    mequipcat = models.TextField(max_length=10, null=True)
    mequiptype = models.TextField(max_length=10, null=True)
    mequipnotes = models.CharField(max_length=1)
    triggerdate = models.TextField(max_length=10, null=True)
    reqcampusid = models.TextField(max_length=10, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    numperiods = models.BigIntegerField(null=True, blank=True)
    maxperiodgap = models.BigIntegerField(null=True, blank=True)
    groupid = models.BigIntegerField(null=True, blank=True)
    tobescheduled = models.BigIntegerField(null=True, blank=True)
    board = models.TextField(max_length=10, null=True)
    series = models.TextField(max_length=10, null=True)
    crsyear = models.TextField(max_length=4, null=True)
    optcode = models.TextField(max_length=10, null=True)
    compcode = models.TextField(max_length=20, null=True)
    subcode = models.TextField(max_length=10, null=True)
    compinstid = models.BigIntegerField(null=True, blank=True)
    roompoolid = models.BigIntegerField(null=True, blank=True)
    nonconid = models.BigIntegerField(null=True, blank=True)
    typeevent = models.BigIntegerField(null=True, blank=True)
    ncyear = models.TextField(max_length=3, null=True)
    reasonforchange = models.TextField(max_length=10, null=True)

    class Meta:
        _DATABASE = 'gencache'


class TimetableB(models.Model):
    id = models.AutoField(primary_key=True)
    slotid = models.BigIntegerField(null=True, blank=True)
    slotentry = models.BigIntegerField(null=True, blank=True)
    slottotal = models.BigIntegerField(null=True, blank=True)
    setid = models.TextField(max_length=10)
    periodid = models.BigIntegerField(null=True, blank=True)
    weekday = models.BigIntegerField(null=True, blank=True)
    starttime = models.TextField(max_length=5, null=True)
    duration = models.BigIntegerField(null=True, blank=True)
    finishtime = models.TextField(max_length=5, null=True)
    weekid = models.BigIntegerField(null=True, blank=True)
    classgroupid = models.TextField(max_length=10, null=True)
    courseid = models.TextField(max_length=12, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    clsgrpcode = models.TextField(max_length=10, null=True)
    lecturerid = models.TextField(max_length=10, null=True)
    moduleid = models.TextField(max_length=12, null=True)
    deptid = models.TextField(max_length=10, null=True)
    moduletype = models.TextField(max_length=10, null=True)
    modgrpcode = models.TextField(max_length=10, null=True)
    siteid = models.TextField(max_length=10, null=True)
    roomid = models.TextField(max_length=10, null=True)
    roomgrpcode = models.TextField(max_length=10, null=True)
    sourcesid = models.TextField(max_length=20, null=True)
    capacity = models.BigIntegerField(null=True, blank=True)
    reqsiteid = models.TextField(max_length=10, null=True)
    reqroomid = models.TextField(max_length=10, null=True)
    reqtype = models.TextField(max_length=10, null=True)
    reqcategory = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=10, null=True)
    linkid = models.BigIntegerField(null=True, blank=True)
    chainid = models.BigIntegerField(null=True, blank=True)
    exclid = models.BigIntegerField(null=True, blank=True)
    associd = models.BigIntegerField(null=True, blank=True)
    specid = models.BigIntegerField(null=True, blank=True)
    locked = models.BigIntegerField(null=True, blank=True)
    status = models.BigIntegerField(null=True, blank=True)
    readlock = models.BigIntegerField(null=True, blank=True)
    classif = models.TextField(max_length=10, null=True)
    owner = models.TextField(max_length=10, null=True)
    drstatus = models.BigIntegerField(null=True, blank=True)
    lectgrp = models.BigIntegerField(null=True, blank=True)
    evpriority = models.BigIntegerField(null=True, blank=True)
    fixlect = models.CharField(max_length=1, null=True)
    fixroom = models.CharField(max_length=1, null=True)
    fixevent = models.CharField(max_length=1)
    reqclass = models.TextField(max_length=10, null=True)
    reqzone = models.TextField(max_length=10, null=True)
    tweightid = models.BigIntegerField(null=True, blank=True)
    fixweight = models.BigIntegerField(null=True, blank=True)
    siteproximity = models.BigIntegerField(null=True, blank=True)
    zoneproximity = models.BigIntegerField(null=True, blank=True)
    maxrooms = models.BigIntegerField(null=True, blank=True)
    datechanged = models.TextField(max_length=12, null=True)
    sizeused = models.BigIntegerField(null=True, blank=True)
    # uniquefield has null values in, so we have to account for this
    uniquefield = models.TextField(max_length=10, null=True)
    equipid = models.TextField(max_length=10, null=True)
    ecode = models.TextField(max_length=20, null=True)
    einstalled = models.TextField(max_length=12, null=True)
    eremoved = models.TextField(max_length=12, null=True)
    ewhoinstalled = models.TextField(max_length=20, null=True)
    ewhoremoved = models.TextField(max_length=20, null=True)
    tobecopied = models.CharField(max_length=1, null=True)
    copied = models.CharField(max_length=1, null=True)
    excludefit = models.CharField(max_length=1, null=True)
    gendatanum = models.BigIntegerField(null=True, blank=True)
    gendatastring = models.TextField(max_length=100, null=True)
    regid = models.BigIntegerField(null=True, blank=True)
    sourcechange = models.BigIntegerField(null=True, blank=True)
    userchange = models.TextField(max_length=30, null=True)
    mequipcat = models.TextField(max_length=10, null=True)
    mequiptype = models.TextField(max_length=10, null=True)
    mequipnotes = models.CharField(max_length=1)
    triggerdate = models.TextField(max_length=10, null=True)
    reqcampusid = models.TextField(max_length=10, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    numperiods = models.BigIntegerField(null=True, blank=True)
    maxperiodgap = models.BigIntegerField(null=True, blank=True)
    groupid = models.BigIntegerField(null=True, blank=True)
    tobescheduled = models.BigIntegerField(null=True, blank=True)
    board = models.TextField(max_length=10, null=True)
    series = models.TextField(max_length=10, null=True)
    crsyear = models.TextField(max_length=4, null=True)
    optcode = models.TextField(max_length=10, null=True)
    compcode = models.TextField(max_length=20, null=True)
    subcode = models.TextField(max_length=10, null=True)
    compinstid = models.BigIntegerField(null=True, blank=True)
    roompoolid = models.BigIntegerField(null=True, blank=True)
    nonconid = models.BigIntegerField(null=True, blank=True)
    typeevent = models.BigIntegerField(null=True, blank=True)
    ncyear = models.TextField(max_length=3, null=True)
    reasonforchange = models.TextField(max_length=10, null=True)

    class Meta:
        _DATABASE = 'gencache'


class Stumodules(models.Model):
    setid = models.TextField(max_length=10)
    studentid = models.TextField(primary_key=True, max_length=12)
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    modgrpcode = models.TextField(max_length=10, null=True)
    slotid = models.BigIntegerField(null=True, blank=True)
    fixingrp = models.CharField(max_length=1, null=True)
    modpart = models.TextField(max_length=10, null=True)
    restype = models.TextField(max_length=10, null=True)
    unitvalue = models.TextField(max_length=10, null=True)
    classif = models.TextField(max_length=10, null=True)
    papernum = models.BigIntegerField(null=True, blank=True)
    modlevel = models.TextField(max_length=10, null=True)
    inactive = models.CharField(max_length=1, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    courseid = models.TextField(max_length=12, null=True)
    crsyear = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    moddropped = models.CharField(max_length=1, null=True)
    donotcount = models.CharField(max_length=1, null=True)
    semrank = models.BigIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."STUMODULES"'
        _DATABASE = 'roombookings'


class StumodulesA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    studentid = models.TextField(max_length=12)
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    modgrpcode = models.TextField(max_length=10, null=True)
    slotid = models.BigIntegerField(null=True, blank=True)
    fixingrp = models.CharField(max_length=1, null=True)
    modpart = models.TextField(max_length=10, null=True)
    restype = models.TextField(max_length=10, null=True)
    unitvalue = models.TextField(max_length=10, null=True)
    classif = models.TextField(max_length=10, null=True)
    papernum = models.BigIntegerField(null=True, blank=True)
    modlevel = models.TextField(max_length=10, null=True)
    inactive = models.CharField(max_length=1, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    courseid = models.TextField(max_length=12, null=True)
    crsyear = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    moddropped = models.CharField(max_length=1, null=True)
    donotcount = models.CharField(max_length=1, null=True)
    semrank = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class StumodulesB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    studentid = models.TextField(max_length=12)
    deptid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    modgrpcode = models.TextField(max_length=10, null=True)
    slotid = models.BigIntegerField(null=True, blank=True)
    fixingrp = models.CharField(max_length=1, null=True)
    modpart = models.TextField(max_length=10, null=True)
    restype = models.TextField(max_length=10, null=True)
    unitvalue = models.TextField(max_length=10, null=True)
    classif = models.TextField(max_length=10, null=True)
    papernum = models.BigIntegerField(null=True, blank=True)
    modlevel = models.TextField(max_length=10, null=True)
    inactive = models.CharField(max_length=1, null=True)
    instid = models.BigIntegerField(null=True, blank=True)
    courseid = models.TextField(max_length=12, null=True)
    crsyear = models.BigIntegerField(null=True, blank=True)
    semid = models.BigIntegerField(null=True, blank=True)
    moddropped = models.CharField(max_length=1, null=True)
    donotcount = models.CharField(max_length=1, null=True)
    semrank = models.BigIntegerField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Features(models.Model):
    setid = models.TextField(max_length=10)
    featureid = models.TextField(max_length=10)
    description = models.TextField(primary_key=True, max_length=80)
    linkcode = models.TextField(max_length=20)
    contactid = models.TextField(max_length=10)
    cost = models.TextField(max_length=10)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."FEATURES"'
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
        db_table = '"CMIS_OWNER"."EQUIPMENT"'
        _DATABASE = 'roombookings'


class Course(models.Model):
    setid = models.TextField(max_length=10)
    courseid = models.TextField(primary_key=True, max_length=12)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20)
    owner = models.TextField(max_length=10)
    numyears = models.BigIntegerField(null=True, blank=True)
    crsweight = models.FloatField(null=True)
    minmodules = models.BigIntegerField(null=True, blank=True)
    maxmodules = models.BigIntegerField(null=True, blank=True)
    numplaces = models.BigIntegerField(null=True, blank=True)
    mintotal = models.BigIntegerField(null=True, blank=True)
    maxtotal = models.BigIntegerField(null=True, blank=True)
    firstyear = models.BigIntegerField(null=True, blank=True)
    oldcourseid = models.TextField(max_length=12, null=True)
    isactive = models.CharField(max_length=1, null=True)
    lecturerid = models.TextField(max_length=10, null=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."COURSE"'
        _DATABASE = 'roombookings'


class CourseA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20)
    owner = models.TextField(max_length=10)
    numyears = models.IntegerField()
    crsweight = models.FloatField(null=True, blank=True)
    minmodules = models.IntegerField(null=True, blank=True)
    maxmodules = models.IntegerField(null=True, blank=True)
    numplaces = models.IntegerField(null=True, blank=True)
    mintotal = models.IntegerField(null=True, blank=True)
    maxtotal = models.IntegerField(null=True, blank=True)
    firstyear = models.IntegerField(null=True, blank=True)
    oldcourseid = models.TextField(max_length=12, null=True, blank=True)
    isactive = models.CharField(max_length=1, null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class CourseB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    courseid = models.TextField(max_length=12)
    name = models.TextField(max_length=80)
    category = models.TextField(max_length=10)
    type = models.TextField(max_length=10, null=True)
    linkcode = models.TextField(max_length=20)
    owner = models.TextField(max_length=10)
    numyears = models.IntegerField()
    crsweight = models.FloatField(null=True, blank=True)
    minmodules = models.IntegerField(null=True, blank=True)
    maxmodules = models.IntegerField(null=True, blank=True)
    numplaces = models.IntegerField(null=True, blank=True)
    mintotal = models.IntegerField(null=True, blank=True)
    maxtotal = models.IntegerField(null=True, blank=True)
    firstyear = models.IntegerField(null=True, blank=True)
    oldcourseid = models.TextField(max_length=12, null=True, blank=True)
    isactive = models.CharField(max_length=1, null=True, blank=True)
    lecturerid = models.TextField(max_length=10, null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Cminstances(models.Model):
    setid = models.TextField(max_length=10)
    instid = models.BigIntegerField(primary_key=True)
    instcode = models.TextField(max_length=10, null=True, blank=True)
    instname = models.TextField(max_length=40, null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    instrank = models.BigIntegerField(null=True, blank=True)
    inststart = models.DateField(null=True, blank=True)
    instfinish = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."CMINSTANCES"'
        _DATABASE = 'roombookings'


class CminstancesA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    instid = models.BigIntegerField(null=True, blank=True)
    instcode = models.TextField(max_length=10, null=True, blank=True)
    instname = models.TextField(max_length=40, null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    instrank = models.BigIntegerField(null=True, blank=True)
    inststart = models.DateField(null=True, blank=True)
    instfinish = models.DateField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class CminstancesB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    instid = models.BigIntegerField(null=True, blank=True)
    instcode = models.TextField(max_length=10, null=True, blank=True)
    instname = models.TextField(max_length=40, null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    instrank = models.BigIntegerField(null=True, blank=True)
    inststart = models.DateField(null=True, blank=True)
    instfinish = models.DateField(null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Modulegroups(models.Model):
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    owner = models.TextField(max_length=10)
    grpcode = models.TextField(max_length=10)
    name = models.TextField(max_length=30, null=True, blank=True)
    csize = models.IntegerField(null=True, blank=True)
    minsize = models.IntegerField(null=True, blank=True)
    maxsize = models.IntegerField(null=True, blank=True)
    prefmaxsize = models.IntegerField(null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    estsize = models.IntegerField(null=True, blank=True)
    thiskey = models.IntegerField(null=True, blank=True)
    parentkey = models.IntegerField(null=True, blank=True)
    groupnum = models.IntegerField(null=True, blank=True)
    mequivid = models.IntegerField(null=True, blank=True)
    instid = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."MODULEGROUPS"'
        _DATABASE = 'roombookings'
        unique_together = (("setid", "moduleid", "grpcode"),)


class ModulegroupsA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    owner = models.TextField(max_length=10)
    grpcode = models.TextField(max_length=10)
    name = models.TextField(max_length=30, null=True, blank=True)
    csize = models.IntegerField(null=True, blank=True)
    minsize = models.IntegerField(null=True, blank=True)
    maxsize = models.IntegerField(null=True, blank=True)
    prefmaxsize = models.IntegerField(null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    estsize = models.IntegerField(null=True, blank=True)
    thiskey = models.IntegerField(null=True, blank=True)
    parentkey = models.IntegerField(null=True, blank=True)
    groupnum = models.IntegerField(null=True, blank=True)
    mequivid = models.IntegerField(null=True, blank=True)
    instid = models.IntegerField()

    class Meta:
        _DATABASE = 'gencache'


class ModulegroupsB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    moduleid = models.TextField(max_length=12)
    owner = models.TextField(max_length=10)
    grpcode = models.TextField(max_length=10)
    name = models.TextField(max_length=30, null=True, blank=True)
    csize = models.IntegerField(null=True, blank=True)
    minsize = models.IntegerField(null=True, blank=True)
    maxsize = models.IntegerField(null=True, blank=True)
    prefmaxsize = models.IntegerField(null=True, blank=True)
    linkcode = models.TextField(max_length=20, null=True, blank=True)
    estsize = models.IntegerField(null=True, blank=True)
    thiskey = models.IntegerField(null=True, blank=True)
    parentkey = models.IntegerField(null=True, blank=True)
    groupnum = models.IntegerField(null=True, blank=True)
    mequivid = models.IntegerField(null=True, blank=True)
    instid = models.IntegerField()

    class Meta:
        _DATABASE = 'gencache'


class Stuclasses(models.Model):
    setid = models.TextField(max_length=10)
    studentid = models.TextField(primary_key=True, max_length=12)
    courseid = models.TextField(max_length=12)
    classgroupid = models.TextField(max_length=10)
    clsgrpcode = models.TextField(max_length=10, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    fixingrp = models.CharField(max_length=1, null=True, blank=True)
    inactive = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"CMIS_OWNER"."STUCLASSES"'
        _DATABASE = 'roombookings'


class StuclassesA(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    studentid = models.TextField(max_length=12)
    courseid = models.TextField(max_length=12)
    classgroupid = models.TextField(max_length=10)
    clsgrpcode = models.TextField(max_length=10, null=True)
    courseyear = models.BigIntegerField(null=True, blank=True)
    fixingrp = models.CharField(max_length=1, null=True, blank=True)
    inactive = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class StuclassesB(models.Model):
    id = models.AutoField(primary_key=True)
    setid = models.TextField(max_length=10)
    studentid = models.TextField(max_length=12)
    courseid = models.TextField(max_length=12)
    classgroupid = models.TextField(max_length=10)
    clsgrpcode = models.TextField(max_length=10)
    courseyear = models.BigIntegerField(null=True, blank=True)
    fixingrp = models.CharField(max_length=1, null=True, blank=True)
    inactive = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        _DATABASE = 'gencache'


class Lock(models.Model):
    a = models.BooleanField()
    b = models.BooleanField()

    class Meta:
        _DATABASE = 'default'

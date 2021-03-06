from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LecturerA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('lecturerid', models.TextField(max_length=10)),
                ('name', models.TextField(max_length=80)),
                ('category', models.TextField(max_length=10)),
                ('type', models.TextField(max_length=10)),
                ('status', models.TextField(max_length=10)),
                ('parttime', models.TextField(max_length=20)),
                ('cost', models.BigIntegerField()),
                ('costtype', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=20)),
                ('owner', models.TextField(max_length=10)),
                ('displectid', models.TextField(max_length=10, serialize=False)),
                ('covprior', models.BigIntegerField()),
                ('covingprior', models.BigIntegerField()),
                ('excludecover', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LecturerB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('lecturerid', models.TextField(max_length=10)),
                ('name', models.TextField(max_length=80)),
                ('category', models.TextField(max_length=10)),
                ('type', models.TextField(max_length=10)),
                ('status', models.TextField(max_length=10)),
                ('parttime', models.TextField(max_length=20)),
                ('cost', models.BigIntegerField()),
                ('costtype', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=20)),
                ('owner', models.TextField(max_length=10)),
                ('displectid', models.TextField(max_length=10, serialize=False)),
                ('covprior', models.BigIntegerField()),
                ('covingprior', models.BigIntegerField()),
                ('excludecover', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.BooleanField()),
                ('b', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ModuleA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('moduleid', models.TextField(max_length=12, serialize=False)),
                ('owner', models.TextField(max_length=10)),
                ('name', models.TextField(max_length=120)),
                ('category', models.TextField(max_length=10)),
                ('classif', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=20)),
                ('csize', models.BigIntegerField()),
                ('minsize', models.BigIntegerField()),
                ('maxsize', models.BigIntegerField()),
                ('prefmaxsize', models.BigIntegerField()),
                ('lecturerid', models.TextField(max_length=10)),
                ('lectgroup', models.BigIntegerField()),
                ('dontfit', models.CharField(max_length=1)),
                ('unitvalue', models.TextField(max_length=10)),
                ('instid', models.BigIntegerField()),
                ('isactive', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('moduleid', models.TextField(max_length=12, serialize=False)),
                ('owner', models.TextField(max_length=10)),
                ('name', models.TextField(max_length=120)),
                ('category', models.TextField(max_length=10)),
                ('classif', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=20)),
                ('csize', models.BigIntegerField()),
                ('minsize', models.BigIntegerField()),
                ('maxsize', models.BigIntegerField()),
                ('prefmaxsize', models.BigIntegerField()),
                ('lecturerid', models.TextField(max_length=10)),
                ('lectgroup', models.BigIntegerField()),
                ('dontfit', models.CharField(max_length=1)),
                ('unitvalue', models.TextField(max_length=10)),
                ('instid', models.BigIntegerField()),
                ('isactive', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='RoomsA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomid', models.TextField(max_length=10)),
                ('siteid', models.TextField(max_length=10)),
                ('name', models.TextField(max_length=80)),
                ('category', models.TextField(max_length=10)),
                ('type', models.TextField(max_length=10)),
                ('classification', models.TextField(max_length=10, serialize=False)),
                ('roomgrpcode', models.TextField(max_length=10)),
                ('zone', models.TextField(max_length=10)),
                ('capacity', models.BigIntegerField()),
                ('prefmin', models.BigIntegerField()),
                ('prefmax', models.BigIntegerField()),
                ('deptid', models.TextField(max_length=10)),
                ('roomarea', models.BigIntegerField()),
                ('dynafill', models.CharField(max_length=1)),
                ('setid', models.TextField(max_length=10)),
                ('uniquefield', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=20)),
                ('campusid', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RoomsB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomid', models.TextField(max_length=10)),
                ('siteid', models.TextField(max_length=10)),
                ('name', models.TextField(max_length=80)),
                ('category', models.TextField(max_length=10)),
                ('type', models.TextField(max_length=10)),
                ('classification', models.TextField(max_length=10, serialize=False)),
                ('roomgrpcode', models.TextField(max_length=10)),
                ('zone', models.TextField(max_length=10)),
                ('capacity', models.BigIntegerField()),
                ('prefmin', models.BigIntegerField()),
                ('prefmax', models.BigIntegerField()),
                ('deptid', models.TextField(max_length=10)),
                ('roomarea', models.BigIntegerField()),
                ('dynafill', models.CharField(max_length=1)),
                ('setid', models.TextField(max_length=10)),
                ('uniquefield', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=20)),
                ('campusid', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SitesA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('siteid', models.TextField(max_length=10)),
                ('sitename', models.TextField(max_length=80)),
                ('address1', models.TextField(max_length=80)),
                ('address2', models.TextField(max_length=80, serialize=False)),
                ('address3', models.TextField(max_length=80)),
                ('address4', models.TextField(max_length=80)),
                ('phone1', models.TextField(max_length=50)),
                ('phone2', models.TextField(max_length=50)),
                ('contact1', models.TextField(max_length=50)),
                ('contact2', models.TextField(max_length=50)),
                ('linkcode', models.TextField(max_length=20)),
                ('campusid', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SitesB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('siteid', models.TextField(max_length=10)),
                ('sitename', models.TextField(max_length=80)),
                ('address1', models.TextField(max_length=80)),
                ('address2', models.TextField(max_length=80, serialize=False)),
                ('address3', models.TextField(max_length=80)),
                ('address4', models.TextField(max_length=80)),
                ('phone1', models.TextField(max_length=50)),
                ('phone2', models.TextField(max_length=50)),
                ('contact1', models.TextField(max_length=50)),
                ('contact2', models.TextField(max_length=50)),
                ('linkcode', models.TextField(max_length=20)),
                ('campusid', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TimetableA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slotid', models.BigIntegerField(serialize=False)),
                ('slotentry', models.BigIntegerField()),
                ('slottotal', models.BigIntegerField()),
                ('setid', models.TextField(max_length=10)),
                ('periodid', models.BigIntegerField()),
                ('weekday', models.BigIntegerField()),
                ('starttime', models.TextField(max_length=5)),
                ('duration', models.BigIntegerField()),
                ('finishtime', models.TextField(max_length=5)),
                ('weekid', models.BigIntegerField()),
                ('classgroupid', models.TextField(max_length=10)),
                ('courseid', models.TextField(max_length=12)),
                ('courseyear', models.BigIntegerField()),
                ('clsgrpcode', models.TextField(max_length=10)),
                ('lecturerid', models.TextField(max_length=10)),
                ('moduleid', models.TextField(max_length=12)),
                ('deptid', models.TextField(max_length=10)),
                ('moduletype', models.TextField(max_length=10)),
                ('modgrpcode', models.TextField(max_length=10)),
                ('siteid', models.TextField(max_length=10)),
                ('roomid', models.TextField(max_length=10)),
                ('roomgrpcode', models.TextField(max_length=10)),
                ('sourcesid', models.TextField(max_length=20)),
                ('capacity', models.BigIntegerField()),
                ('reqsiteid', models.TextField(max_length=10)),
                ('reqroomid', models.TextField(max_length=10)),
                ('reqtype', models.TextField(max_length=10)),
                ('reqcategory', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=10)),
                ('linkid', models.BigIntegerField()),
                ('chainid', models.BigIntegerField()),
                ('exclid', models.BigIntegerField()),
                ('associd', models.BigIntegerField()),
                ('specid', models.BigIntegerField()),
                ('locked', models.BigIntegerField()),
                ('status', models.BigIntegerField()),
                ('readlock', models.BigIntegerField()),
                ('classif', models.TextField(max_length=10)),
                ('owner', models.TextField(max_length=10)),
                ('drstatus', models.BigIntegerField()),
                ('lectgrp', models.BigIntegerField()),
                ('evpriority', models.BigIntegerField()),
                ('fixlect', models.CharField(max_length=1)),
                ('fixroom', models.CharField(max_length=1)),
                ('fixevent', models.CharField(max_length=1)),
                ('reqclass', models.TextField(max_length=10)),
                ('reqzone', models.TextField(max_length=10)),
                ('tweightid', models.BigIntegerField()),
                ('fixweight', models.BigIntegerField()),
                ('siteproximity', models.BigIntegerField()),
                ('zoneproximity', models.BigIntegerField()),
                ('maxrooms', models.BigIntegerField()),
                ('datechanged', models.TextField(max_length=12)),
                ('sizeused', models.BigIntegerField()),
                ('uniquefield', models.TextField(max_length=10)),
                ('equipid', models.TextField(max_length=10)),
                ('ecode', models.TextField(max_length=20)),
                ('einstalled', models.TextField(max_length=12)),
                ('eremoved', models.TextField(max_length=12)),
                ('ewhoinstalled', models.TextField(max_length=20)),
                ('ewhoremoved', models.TextField(max_length=20)),
                ('tobecopied', models.CharField(max_length=1)),
                ('copied', models.CharField(max_length=1)),
                ('excludefit', models.CharField(max_length=1)),
                ('gendatanum', models.BigIntegerField()),
                ('gendatastring', models.TextField(max_length=100)),
                ('regid', models.BigIntegerField()),
                ('sourcechange', models.BigIntegerField()),
                ('userchange', models.TextField(max_length=30)),
                ('mequipcat', models.TextField(max_length=10)),
                ('mequiptype', models.TextField(max_length=10)),
                ('mequipnotes', models.CharField(max_length=1)),
                ('triggerdate', models.TextField(max_length=10)),
                ('reqcampusid', models.TextField(max_length=10)),
                ('instid', models.BigIntegerField()),
                ('numperiods', models.BigIntegerField()),
                ('maxperiodgap', models.BigIntegerField()),
                ('groupid', models.BigIntegerField()),
                ('tobescheduled', models.BigIntegerField()),
                ('board', models.TextField(max_length=10)),
                ('series', models.TextField(max_length=10)),
                ('crsyear', models.TextField(max_length=4)),
                ('optcode', models.TextField(max_length=10)),
                ('compcode', models.TextField(max_length=20)),
                ('subcode', models.TextField(max_length=10)),
                ('compinstid', models.BigIntegerField()),
                ('roompoolid', models.BigIntegerField()),
                ('nonconid', models.BigIntegerField()),
                ('typeevent', models.BigIntegerField()),
                ('ncyear', models.TextField(max_length=3)),
                ('reasonforchange', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TimetableB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slotid', models.BigIntegerField(serialize=False)),
                ('slotentry', models.BigIntegerField()),
                ('slottotal', models.BigIntegerField()),
                ('setid', models.TextField(max_length=10)),
                ('periodid', models.BigIntegerField()),
                ('weekday', models.BigIntegerField()),
                ('starttime', models.TextField(max_length=5)),
                ('duration', models.BigIntegerField()),
                ('finishtime', models.TextField(max_length=5)),
                ('weekid', models.BigIntegerField()),
                ('classgroupid', models.TextField(max_length=10)),
                ('courseid', models.TextField(max_length=12)),
                ('courseyear', models.BigIntegerField()),
                ('clsgrpcode', models.TextField(max_length=10)),
                ('lecturerid', models.TextField(max_length=10)),
                ('moduleid', models.TextField(max_length=12)),
                ('deptid', models.TextField(max_length=10)),
                ('moduletype', models.TextField(max_length=10)),
                ('modgrpcode', models.TextField(max_length=10)),
                ('siteid', models.TextField(max_length=10)),
                ('roomid', models.TextField(max_length=10)),
                ('roomgrpcode', models.TextField(max_length=10)),
                ('sourcesid', models.TextField(max_length=20)),
                ('capacity', models.BigIntegerField()),
                ('reqsiteid', models.TextField(max_length=10)),
                ('reqroomid', models.TextField(max_length=10)),
                ('reqtype', models.TextField(max_length=10)),
                ('reqcategory', models.TextField(max_length=10)),
                ('linkcode', models.TextField(max_length=10)),
                ('linkid', models.BigIntegerField()),
                ('chainid', models.BigIntegerField()),
                ('exclid', models.BigIntegerField()),
                ('associd', models.BigIntegerField()),
                ('specid', models.BigIntegerField()),
                ('locked', models.BigIntegerField()),
                ('status', models.BigIntegerField()),
                ('readlock', models.BigIntegerField()),
                ('classif', models.TextField(max_length=10)),
                ('owner', models.TextField(max_length=10)),
                ('drstatus', models.BigIntegerField()),
                ('lectgrp', models.BigIntegerField()),
                ('evpriority', models.BigIntegerField()),
                ('fixlect', models.CharField(max_length=1)),
                ('fixroom', models.CharField(max_length=1)),
                ('fixevent', models.CharField(max_length=1)),
                ('reqclass', models.TextField(max_length=10)),
                ('reqzone', models.TextField(max_length=10)),
                ('tweightid', models.BigIntegerField()),
                ('fixweight', models.BigIntegerField()),
                ('siteproximity', models.BigIntegerField()),
                ('zoneproximity', models.BigIntegerField()),
                ('maxrooms', models.BigIntegerField()),
                ('datechanged', models.TextField(max_length=12)),
                ('sizeused', models.BigIntegerField()),
                ('uniquefield', models.TextField(max_length=10)),
                ('equipid', models.TextField(max_length=10)),
                ('ecode', models.TextField(max_length=20)),
                ('einstalled', models.TextField(max_length=12)),
                ('eremoved', models.TextField(max_length=12)),
                ('ewhoinstalled', models.TextField(max_length=20)),
                ('ewhoremoved', models.TextField(max_length=20)),
                ('tobecopied', models.CharField(max_length=1)),
                ('copied', models.CharField(max_length=1)),
                ('excludefit', models.CharField(max_length=1)),
                ('gendatanum', models.BigIntegerField()),
                ('gendatastring', models.TextField(max_length=100)),
                ('regid', models.BigIntegerField()),
                ('sourcechange', models.BigIntegerField()),
                ('userchange', models.TextField(max_length=30)),
                ('mequipcat', models.TextField(max_length=10)),
                ('mequiptype', models.TextField(max_length=10)),
                ('mequipnotes', models.CharField(max_length=1)),
                ('triggerdate', models.TextField(max_length=10)),
                ('reqcampusid', models.TextField(max_length=10)),
                ('instid', models.BigIntegerField()),
                ('numperiods', models.BigIntegerField()),
                ('maxperiodgap', models.BigIntegerField()),
                ('groupid', models.BigIntegerField()),
                ('tobescheduled', models.BigIntegerField()),
                ('board', models.TextField(max_length=10)),
                ('series', models.TextField(max_length=10)),
                ('crsyear', models.TextField(max_length=4)),
                ('optcode', models.TextField(max_length=10)),
                ('compcode', models.TextField(max_length=20)),
                ('subcode', models.TextField(max_length=10)),
                ('compinstid', models.BigIntegerField()),
                ('roompoolid', models.BigIntegerField()),
                ('nonconid', models.BigIntegerField()),
                ('typeevent', models.BigIntegerField()),
                ('ncyear', models.TextField(max_length=3)),
                ('reasonforchange', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WeekmapnumericA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10, serialize=False)),
                ('weekid', models.BigIntegerField()),
                ('weeknumber', models.BigIntegerField()),
                ('drstatus', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeekmapnumericB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10, serialize=False)),
                ('weekid', models.BigIntegerField()),
                ('weeknumber', models.BigIntegerField()),
                ('drstatus', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeekmapstringA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('weekid', models.BigIntegerField()),
                ('name', models.TextField(max_length=50)),
                ('weeks', models.TextField(max_length=104)),
                ('numweeks', models.BigIntegerField()),
                ('statweeks', models.TextField(max_length=10, serialize=False)),
                ('drstatus', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeekmapstringB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('weekid', models.BigIntegerField()),
                ('name', models.TextField(max_length=50)),
                ('weeks', models.TextField(max_length=104)),
                ('numweeks', models.BigIntegerField()),
                ('statweeks', models.TextField(max_length=10, serialize=False)),
                ('drstatus', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeekstructureA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('weeknumber', models.BigIntegerField()),
                ('startdate', models.DateField()),
                ('description', models.TextField(max_length=80, serialize=False)),
                ('mappedto', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeekstructureB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.TextField(max_length=10)),
                ('weeknumber', models.BigIntegerField()),
                ('startdate', models.DateField()),
                ('description', models.TextField(max_length=80, serialize=False)),
                ('mappedto', models.BigIntegerField()),
            ],
        ),
    ]
class ModelRouter(object):
    def __init__(self):
        self.managed_db_list = ['default', 'gencache']
        self.gencache_model_names = [
            "bookinga",
            "bookingb",
            "rooma",
            "roomb",
            "cminstancesa",
            "cminstancesb",
            "coursea",
            "courseb",
            "crsavailmodulesa",
            "crsavailmodulesb",
            "crscompmodulesa",
            "crscompmodulesb",
            "lecturera",
            "lecturerb",
            "modulea",
            "moduleb",
            "modulegroupsa",
            "modulegroupsb",
            "roomsa",
            "roomsb",
            "sitesa",
            "sitesb",
            "timetablea",
            "timetableb",
            "weekmapnumerica",
            "weekmapnumericb",
            "weekmapstringa",
            "weekmapstringb",
            "weekstructurea",
            "weekstructureb",
            "studentsa",
            "studentsb",
            "stuclassesa",
            "stuclassesb",
            "stumodulesa",
            "stumodulesb",
            "deptsa",
            "deptsb",
            "coursea",
            "courseb",
            "crsavailmodulesa",
            "crsavailmodulesb",
            "crscompmodulesa",
            "crscompmodulesb"
        ]

    def db_for_read(self, model, **hints):
        return getattr(model._meta, "_DATABASE", "default")

    def db_for_write(self, model, **hints):
        return getattr(model._meta, "_DATABASE", "default")

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._state.db in self.managed_db_list and \
               obj2._state.db in self.managed_db_list

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Special rule for stored functions in the Timetable app
        if (
            app_label == "timetable" and
            model_name == None and
            "type" in hints and
            hints["type"] == "raw_sql"
        ):
            return db == "gencache"

        if db == "default":
            return model_name not in self.gencache_model_names

        elif db == "gencache":
            return model_name in self.gencache_model_names

        return False

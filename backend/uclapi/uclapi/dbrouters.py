class ModelRouter(object):
    def __init__(self):
        self.managed_db_list = ['default', 'gencache']

    def db_for_read(self, model, **hints):
        return getattr(model._meta, "_DATABASE", "default")

    def db_for_write(self, model, **hints):
        return getattr(model._meta, "_DATABASE", "default")

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._state.db in self.managed_db_list and obj2._state.db in self.managed_db_list

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "default":
            if (model_name == "bookinga") or (model_name == "bookingb"):
                return False
            else:
                return True
        elif db == "gencache":
            if (model_name == "bookinga") or (model_name == "bookingb"):
                return True
            else:
                return False
        return False



class JournalsRouter:
    route_app_labels = {'journals', }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'journals'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'journals'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label or  obj2._meta.app_label in self.route_app_labels:
            return True
        elif self.route_app_labels not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'journals'
        return None
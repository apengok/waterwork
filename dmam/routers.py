
class DmamRouter:
    """
    A router to control all database operations on models in the
    water application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read water models go to water.
        """
        if model._meta.app_label == 'dmam':
            return 'zncb'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write water models go to water.
        """
        if model._meta.app_label == 'dmam':
            return 'zncb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the water app is involved.
        """
        if obj1._meta.app_label == 'dmam' or \
           obj2._meta.app_label == 'dmam':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the water app only appears in the 'water'
        database.
        """
        if app_label == 'dmam':
            return db == 'zncb'
        return None
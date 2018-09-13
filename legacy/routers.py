# -*- coding:utf-8 -*-

def decide_on_model(model):
    """Small helper function to pipe all DB operations of a worlddata model to the world_data DB"""
    return 'zncb' if model._meta.app_label == 'legacy' else None


class LegacyRouter:
    """
    Implements a database router so that:

    * Django related data - DB alias `default` - MySQL DB `world_django`
    * Legacy "world" database data (everything "non-Django") - DB alias `world_data` - MySQL DB `world`
    """
    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'legacy' or \
           obj2._meta.app_label == 'dmam':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'legacy':
            return db == 'zncb'
        return None
        


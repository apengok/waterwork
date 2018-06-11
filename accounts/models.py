# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,Group,_user_has_perm
)

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
import json
# python manage.py dumpdata dma --format json --indent 4 > dma/dmadd.json
# python manage.py loaddata dma/dmadd.json 


class MyRolesManager(models.Manager):
    """
    The manager for the auth's Group model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

class MyRoles(Group):
    notes           = models.CharField(max_length=156,blank=True)   
    rid             = models.CharField(max_length=1000,blank=True)   
    permissionTree  = models.CharField(max_length=50000,blank=True)

    objects = MyRolesManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    
class UserManager(BaseUserManager):
    def create_user(self, user_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not user_name:
            raise ValueError('Users must have an user_name')

        user = self.model(
            user_name=user_name #self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            user_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            user_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):

    # email = models.EmailField(
    #     verbose_name='email address',
    #     max_length=255,
    #     unique=True,
    # )
    user_name   = models.CharField(_('user name'), max_length=30, unique=True)
    real_name    = models.CharField(_('real name'), max_length=30, blank=True)
    sex          = models.CharField(_('Sex'), max_length=30, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=30, blank=True)
    belongto     = models.CharField(_('belongs to'), max_length=30, blank=True)
    expire_date  = models.CharField(_('Expired date'), max_length=30, blank=True)
    Role         = models.CharField(_('Role'), max_length=30, blank=True)
    # Role        = models.ForeignKey(Roles,related_name='user',on_delete=models.CASCADE)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank=True,
    )
    # BOOL_CHOICES = ((True, '启用'), (False, '停止'))
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.user_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.user_name

    def __str__(self):              # __unicode__ on Python 2
        return self.user_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if not self.is_active:
            return False
        if self.is_admin:
            return True
        return _user_has_perm(self,perm,obj)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def permissiontree(self):

        role = MyRoles.objects.get(name=self.Role)
        try:

            tree = json.loads(role.permissionTree)
            tree_str = [t['id'] for t in tree]
            # return ','.join(tree_str)
            return tree_str
        except:
            return []


    # @property
    # def is_active(self):
    #     "Is the user active?"
    #     return self.active

'''
If you simply subclass the Group object then by default it will create a new database table and the admin site won't pick up any new fields.

You need to inject new fields into the existing Group:
'''
# if not hasattr(Group, 'parent'):
#     field = models.ForeignKey(Group, blank=True, null=True, related_name='children')
#     field.contribute_to_class(Group, 'parent')

# class MyRoles(Group):
#     notes = models.CharField(max_length=156,blank=True)   
#     permissionTree = models.CharField(max_length=50000,blank=True)

# To add methods to the Group, subclass but tag the model as proxy:
    # class Meta:
    #     proxy = True

    # def myFunction(self):
    #     return True

# def post_save_roles_model_receiver(sender,instance,created,*args,**kwargs):
#     if created:
#         try:
#             Roles.objects.create(group=instance)
#         except:
#             pass

# post_save.connect(post_save_roles_model_receiver,sender=Group)  

# class Roles(models.Model):
#     group = models.OneToOneField(Group,on_delete=models.CASCADE)
#     notes = models.CharField(max_length=156,blank=True)   
#     permissionTree = models.CharField(max_length=5000,blank=True)
       
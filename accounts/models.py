# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,Group,_user_has_perm
)

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
import json
from django.db.models import Q

from entm.models import Organizations

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
    """
                      Group.name
    rid:'ROLE_ADMIN',超级管理员
         'POWER_USER',一般管理员
         'ROLE_randomstr',用户创建的角色
    """
    notes           = models.CharField(max_length=156,blank=True)   
    rid             = models.CharField(max_length=1000,blank=True)   #name
    uid             = models.CharField(max_length=100,blank=True)
    permissionTree  = models.CharField(max_length=50000,blank=True)

    belongto     = models.ForeignKey(Organizations,related_name='roles',null=True, blank=True,on_delete=models.CASCADE)

    objects = MyRolesManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class OrganUserQuerySet(models.query.QuerySet):
    def search(self, query): 
        if query:
            query = query.strip()
            return self.filter( #icontains
                Q(idstr__iexact=query)|
                Q(belongto__iexact=query)
                ).distinct()
        return self        

class OrganUserManager(models.Manager):
    def get_queryset(self):
        return OrganUserQuerySet(self.model, using=self._db)

    def search(self, query): 
        return self.get_queryset().search(query)
    
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
    user_name    = models.CharField(verbose_name='用户名', max_length=30, unique=True)
    real_name    = models.CharField(verbose_name='真实姓名', max_length=30, blank=True)
    sex          = models.CharField(verbose_name='性别', max_length=30, blank=True)
    phone_number = models.CharField(verbose_name='手机',  max_length=30, blank=True)
    # belongto     = models.CharField(_('belongs to'), max_length=30, blank=True)
    belongto     = models.ForeignKey(Organizations,verbose_name='所属组织', related_name='users',null=True, blank=True,on_delete=models.CASCADE)
    expire_date  = models.CharField(verbose_name='授权截止日期',  max_length=30, blank=True)
    # Role         = models.CharField(_('Role'), max_length=30, blank=True)
    Role        = models.ForeignKey(MyRoles,verbose_name='角色',related_name='users',null=True, blank=True,on_delete=models.CASCADE)
    idstr       = models.CharField(max_length=300,null=True,blank=True) #(string combind username,group.id,group.pid )
    uuid        = models.CharField(max_length=300,null=True,blank=True)
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        blank=True,
    )
    # BOOL_CHOICES = ((True, '启用'), (False, '停止'))
    is_active = models.BooleanField(verbose_name='启停状态', default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()
    user_in_group = OrganUserManager()

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
        # print('user perm:',perm)
        if not self.is_active:
            return False
        if self.is_admin:
            return True
        return _user_has_perm(self,perm,obj)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_menu_permission(self,perm):
        if self.is_admin:
            return True
        if self.Role is None:
            return False
        permissiontree = self.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            pt_dict[pt["id"]] = pt["edit"]

        if perm in pt_dict.keys():
            return True
        return False

    def has_menu_permission_edit(self,perm):
        if self.is_admin:
            return True
        if self.Role is None:
            return False
        permissiontree = self.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            pt_dict[pt["id"]] = pt["edit"]

        if perm in pt_dict.keys() and pt_dict[perm] == True:
            return True
        return False

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

        # role = MyRoles.objects.get(name=self.Role)
        try:

            tree = json.loads(self.Role.permissionTree)
            tree_str = [t['id'] for t in tree]
            # return ','.join(tree_str)
            return tree_str
        except:
            return []

    def user_list_queryset(self):
        # userlist = []
        if self.is_admin:
            return User.objects.all()

        user_self = User.objects.filter(user_name=self.user_name)
        userlist = user_self
        #下级组织的用户
        sub_organs = self.belongto.sub_organizations(include_self=False)
        # user | merge two QuerySet
        for g in sub_organs:
            userlist |= g.users.all()
            
        return userlist

    def user_list(self):
        userlist = []
        if self.is_admin:
            return User.objects.all()

        userlist.append(self)
        #下级组织的用户
        sub_organs = self.belongto.sub_organizations(include_self=False)
        for g in sub_organs:
            for u in g.users.all():
                userlist.append(u)

        return userlist

    # 返回用户可分配的角色列表
    def role_list(self):
        rolelist = []
        if self.is_admin:
            return MyRoles.objects.all()

        # 自己被分配的角色
        role_self = self.Role
        rolelist.append(role_self)
        
        # 该用户创建的角色
        if MyRoles.objects.filter(uid=self.uuid).exists():
            # Force evaluation of a QuerySet by calling list() on it
            created_by_user = list(MyRoles.objects.filter(uid=self.uuid) )
            
            if created_by_user:
                
                rolelist += created_by_user
                
        #下级组织的角色 和 下级组织的用户的角色
        sub_organs = self.belongto.sub_organizations(include_self=False)
        for g in sub_organs:
            for r in g.roles.all():
                if r and r not in rolelist:
                    rolelist.append(r)
                    
            for u in g.users.all():
                if u.Role and u.Role not in rolelist:
                    rolelist.append(u.Role)
                    
        # print('ret rolelist:',rolelist)
        return rolelist


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
       
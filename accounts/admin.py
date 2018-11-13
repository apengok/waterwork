# -*- coding:utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User,MyRoles

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('user_name','belongto','Role','is_active','expire_date','real_name','sex','phone_number','email','idstr','uuid')
    list_filter = ('admin','is_active')
    
    fieldsets = (
        (None, {'fields': ('user_name','password','belongto','Role','is_active','admin','expire_date','real_name','sex','phone_number','email','idstr','uuid')}),
        
    )

    # fieldsets = (
    #     (None, {'fields': ('user_name', 'password')}),
    #     ('Personal info', {'fields': ()}),
    #     ('Permissions', {'fields': ('admin',)}),
    # )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'password1', 'password2','belongto','Role','is_active','admin','expire_date','real_name','sex','phone_number','email')}
        ),
    )
    search_fields = ('user_name',)
    ordering = ('user_name',)
    filter_horizontal = ()

class MyRoleAdmin(admin.ModelAdmin):
    list_display=  ('name','rid','notes','uid','belongto','permissionTree')

admin.site.register(User, UserAdmin)

admin.site.register(MyRoles,MyRoleAdmin)

admin.site.register(Permission)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

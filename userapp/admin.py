from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
# Register your models here.

class NewUserAdmin(UserAdmin):
    fieldsets = (ad
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('work_number','position','email', 'nickname','company','phone_number','organizationId')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'roles')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    list_display = ('id', 'username', 'company','nickname','position','work_number', 'roles','organization', 'email','phone_number', 'is_active', 'last_login')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email','work_number')

admin.site.register(NewUser, NewUserAdmin)


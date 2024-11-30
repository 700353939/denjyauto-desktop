from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group

from denjyauto.accounts.forms import GroupAdminForm

UserModel = get_user_model()

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel

    password_change_form = PasswordChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_active', 'is_staff'),
        }))

    list_display = ('pk', 'username', 'email', 'date_joined', 'is_client', 'is_active', 'is_staff')
    list_filter = ( 'groups', 'username', 'date_joined')
    list_editable = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('username',)

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']

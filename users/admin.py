from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'email', 'age', 'gender', 'image', 'name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'gender']
    search_fields = ['username', 'email']
    ordering = ['username']

    # Modify fieldsets to only include necessary fields
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'age', 'gender', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Modify add_fieldsets for creating a new user with only required fields
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'age', 'gender', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)

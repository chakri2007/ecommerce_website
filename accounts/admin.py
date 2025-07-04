from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'phone', 'first_name', 'last_name', 'type', 'is_staff')
    list_filter = ('type', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'first_name', 'last_name', 'type', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'phone', 'first_name', 'last_name')
    ordering = ('email',)

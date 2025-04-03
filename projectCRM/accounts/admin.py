from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BusinessUser

class BusinessUserAdmin(UserAdmin):
    list_display = ('company_email', 'company_name', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('company_email', 'company_name')
    readonly_fields = ('id', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    fieldsets = (
        (None, {'fields': ('company_email', 'password')}),
        ('Company Info', {'fields': ('company_name', 'industry', 'job_title', 'employees', 'website', 'address', 'country', 'phone', 'company_logo')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('company_email', 'company_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin'),
        }),
    )

    ordering = ('company_email',)

admin.site.register(BusinessUser, BusinessUserAdmin)

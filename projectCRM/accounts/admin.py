from django.contrib import admin

from .models import BusinessUser

admin.site.register(BusinessUser)

from .models import Role

admin.site.register(Role)

from .models import AccessPermission

admin.site.register(AccessPermission)

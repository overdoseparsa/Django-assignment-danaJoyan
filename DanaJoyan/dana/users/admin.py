from django.contrib import admin

from .models import (
    Admin,
    User,
    UserApp,
)

# Register your models here.

admin.site.register(UserApp)
admin.site.register(Admin)
admin.site.register(User)

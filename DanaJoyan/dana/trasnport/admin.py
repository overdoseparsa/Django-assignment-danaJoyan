from django.contrib import admin

# Register your models here.
from .models import Bus, Company, Seat, Transport

admin.site.register(Company)
admin.site.register(Transport)
admin.site.register(Seat)
admin.site.register(Bus)

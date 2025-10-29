from django.contrib import admin

# Register your models here.

from.models import *

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(ContactMessage)
admin.site.register(Profile)

from django.contrib import admin

from ClientManagement import models

admin.site.register(models.Client)
admin.site.register(models.Attendance)

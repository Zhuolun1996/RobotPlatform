from django.contrib import admin
from .models import server, profile, course,uploadFile

# Register your models here.

admin.site.register(server)
admin.site.register(profile)
admin.site.register(course)
admin.site.register(uploadFile)


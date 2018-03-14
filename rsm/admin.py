from django.contrib import admin
from .models import server, profile, course

# Register your models here.

admin.site.register(server)
admin.site.register(profile)
admin.site.register(course)

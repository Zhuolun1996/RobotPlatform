from django.contrib import admin
from .models import server, profile, course, uploadFile

# Register your models here.

# 在管理后台中注册模型
admin.site.register(server)
admin.site.register(profile)
admin.site.register(course)
admin.site.register(uploadFile)

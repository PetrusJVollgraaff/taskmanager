from django.contrib import admin
from projectsmanager.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Projects)
admin.site.register(Priority)
admin.site.register(Type)
admin.site.register(Tasks)
admin.site.register(TaskAssignTo)
admin.site.register(Log)
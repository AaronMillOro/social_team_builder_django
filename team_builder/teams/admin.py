from django.contrib import admin
from .models import (Profile, Skill, Project, Position)

# Register your models here.
admin.site.register(Position)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Skill)

from django.contrib import admin
from .models import Tree, TaskType, WorkLog

admin.site.register((Tree, TaskType, WorkLog))


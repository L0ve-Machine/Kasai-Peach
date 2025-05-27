from django.contrib import admin
from .models import Tree, TaskType, WorkLog, Cluster, ClusterPhoto  # ← ClusterPhoto を追加

admin.site.register((Tree, TaskType, WorkLog, Cluster, ClusterPhoto))  # ← ClusterPhoto を登録

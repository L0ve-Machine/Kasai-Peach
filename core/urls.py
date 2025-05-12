from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('password/', views.site_password_view, name='site_password'),
    path('accounts/', include('django.contrib.auth.urls')),


    # QR スキャン関連
    path("scan/", views.qr_scan, name="qr_scan"),
    path("scan/success/", views.scan_success, name="scan_success"),
    path("api/scan/start/", views.WorkStartAPI.as_view(), name="api_scan_start"),
    path("api/scan/end/", views.WorkEndAPI.as_view(), name="api_scan_end"),



    path("worklogs/", views.WorkLogListView.as_view(), name="worklog_list"),
    path("fields/<int:field_id>/weather/", views.field_weather_view, name="field_weather"),


    # Tree / Cluster 詳細・QR
    path("tree/<str:qr_id>/", views.tree_detail, name="tree_detail"),
    path("tree/<str:qr_id>/qr.png", views.tree_qr_png, name="tree_qr_png"),
    path("cluster/<int:cluster_id>/", views.cluster_detail, name="cluster_detail"),
    path("cluster/<int:cluster_id>/qr.png", views.cluster_qr_png, name="cluster_qr_png"),


    # Tree CRUD
    path("trees/", views.TreeListView.as_view(), name="tree_list"),
    path("trees/add/", views.TreeCreateView.as_view(), name="tree_add"),
    path("trees/<int:pk>/edit/", views.TreeUpdateView.as_view(), name="tree_edit"),
    path("trees/<int:pk>/delete/", views.TreeDeleteView.as_view(), name="tree_delete"),

    # Cluster CRUD
    path("clusters/", views.ClusterListView.as_view(), name="cluster_list"),
    path("clusters/add/", views.ClusterCreateView.as_view(), name="cluster_add"),
    path("clusters/<int:pk>/edit/", views.ClusterUpdateView.as_view(), name="cluster_edit"),
    path("clusters/<int:pk>/delete/", views.ClusterDeleteView.as_view(), name="cluster_delete"),

    # Variety CRUD
    path("varieties/", views.VarietyListView.as_view(), name="variety_list"),
    path("varieties/add/", views.VarietyCreateView.as_view(), name="variety_add"),
    path("varieties/<int:pk>/edit/", views.VarietyUpdateView.as_view(), name="variety_edit"),
    path("varieties/<int:pk>/delete/", views.VarietyDeleteView.as_view(), name="variety_delete"),

    # Field CRUD
    path("fields/", views.FieldListView.as_view(), name="field_list"),
    path("fields/add/", views.FieldCreateView.as_view(), name="field_add"),
    path("fields/<int:pk>/edit/", views.FieldUpdateView.as_view(), name="field_edit"),
    path("fields/<int:pk>/delete/", views.FieldDeleteView.as_view(), name="field_delete"),

    # TaskType CRUD
    path("tasktypes/", views.TaskTypeListView.as_view(), name="tasktype_list"),
    path("tasktypes/add/", views.TaskTypeCreateView.as_view(), name="tasktype_add"),
    path("tasktypes/<int:pk>/edit/", views.TaskTypeUpdateView.as_view(), name="tasktype_edit"),
    path("tasktypes/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="tasktype_delete"),

    # TaskSchedule CRUD
    path("schedule/<int:variety_id>/", views.TaskScheduleListView.as_view(), name="schedule_list"),
    path("schedule/<int:variety_id>/add/", views.TaskScheduleCreateView.as_view(), name="schedule_add"),
    path("schedule/<int:variety_id>/edit/<int:pk>/", views.TaskScheduleUpdateView.as_view(), name="schedule_edit"),
    path("schedule/<int:variety_id>/delete/<int:pk>/", views.TaskScheduleDeleteView.as_view(), name="schedule_delete"),
]

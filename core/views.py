from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from io import BytesIO
import qrcode
from .forms import WorkLogFilterForm
from datetime import datetime, timedelta, date
from django.db.models import Count, Sum

from .models import (
    Tree, Cluster,
    TaskType, Variety, Field, TaskSchedule, WorkLog
)
from .serializers import WorkLogStartSerializer, WorkLogEndSerializer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class VarietyListView(LoginRequiredMixin, TemplateView):
    template_name = "core/variety_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["peaches"] = Variety.objects.filter(fruit_type="peach").order_by("name")
        ctx["grapes"]  = Variety.objects.filter(fruit_type="grape").order_by("name")
        return ctx
@login_required
def home(request):
    # 🍑 桃・🍇 ぶどうの品種リスト
    peaches = Variety.objects.filter(fruit_type="peach").order_by("name")
    grapes  = Variety.objects.filter(fruit_type="grape").order_by("name")

    # 今日の件数
    today = date.today()
    today_logs = WorkLog.objects.filter(start_at__date=today)
    today_count = today_logs.count()

    # 今月の作業時間（分）
    month_start = today.replace(day=1)
    month_logs = WorkLog.objects.filter(start_at__date__gte=month_start)
    total_seconds = sum(
        (w.end_at - w.start_at).total_seconds()
        for w in month_logs if w.end_at
    )
    total_minutes = int(total_seconds // 60)

    # 作業者別ランキング
    user_ranking = (
        month_logs
        .values("user__username")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    return render(request, "core/home.html", {
        "peaches": peaches,
        "grapes": grapes,
        "today_count": today_count,
        "total_minutes": total_minutes,
        "user_ranking": user_ranking,
    })

@login_required
def qr_scan(request):
    """モバイル用スキャンページ"""
    return render(request, "core/qr_scan.html", {
        "task_types": TaskType.objects.all(),
    })

@login_required
def scan_success(request):
    """登録完了ページ"""
    return render(request, "core/scan_success.html")

@login_required
def tree_detail(request, qr_id):
    """Tree 詳細画面を表示"""
    tree = get_object_or_404(Tree, qr_id=qr_id)
    clusters = tree.cluster_set.all()
    return render(request, "core/tree_detail.html", {
        "tree": tree,
        "clusters": clusters,
    })

@login_required
def cluster_detail(request, cluster_id):
    """Cluster 詳細画面を表示"""
    cluster = get_object_or_404(Cluster, id=cluster_id)
    return render(request, "core/cluster_detail.html", {"cluster": cluster})

@login_required
def tree_qr_png(request, qr_id):
    """Tree 用 QR コードを PNG で返す"""
    buf = BytesIO()
    url = request.build_absolute_uri(reverse("tree_detail", args=[qr_id]))
    qrcode.make(url).save(buf, format="PNG")
    return HttpResponse(buf.getvalue(), content_type="image/png")

@login_required
def cluster_qr_png(request, cluster_id):
    """Cluster 用 QR コードを PNG で返す"""
    buf = BytesIO()
    url = request.build_absolute_uri(reverse("cluster_detail", args=[cluster_id]))
    qrcode.make(url).save(buf, format="PNG")
    return HttpResponse(buf.getvalue(), content_type="image/png")


# ─────────── Class-based CRUD views ───────────

# Tree CRUD
class TreeListView(LoginRequiredMixin, ListView):
    model = Tree
    template_name = "core/tree_list.html"
    context_object_name = "trees"

class TreeCreateView(LoginRequiredMixin, CreateView):
    model = Tree
    fields = ["qr_id", "variety", "field", "age", "planting_date", "transplant_date", "nursery", "training_type"]
    template_name = "core/tree_form.html"
    success_url = reverse_lazy("tree_list")

class TreeUpdateView(LoginRequiredMixin, UpdateView):
    model = Tree
    fields = ["qr_id", "variety", "field", "age", "planting_date", "transplant_date", "nursery", "training_type"]
    template_name = "core/tree_form.html"
    success_url = reverse_lazy("tree_list")

class TreeDeleteView(LoginRequiredMixin, DeleteView):
    model = Tree
    template_name = "core/tree_confirm_delete.html"
    success_url = reverse_lazy("tree_list")

# Cluster CRUD
class ClusterListView(LoginRequiredMixin, ListView):
    model = Cluster
    template_name = "core/cluster_list.html"
    context_object_name = "clusters"

    def get_queryset(self):
        return (
            Cluster.objects
                   .select_related('tree')
                   .order_by('tree__qr_id', 'number')
        )

class ClusterCreateView(LoginRequiredMixin, CreateView):
    model = Cluster
    fields = ["tree", "number"]
    template_name = "core/cluster_form.html"
    success_url = reverse_lazy("cluster_list")

class ClusterUpdateView(LoginRequiredMixin, UpdateView):
    model = Cluster
    fields = ["tree", "number"]
    template_name = "core/cluster_form.html"
    success_url = reverse_lazy("cluster_list")

class ClusterDeleteView(LoginRequiredMixin, DeleteView):
    model = Cluster
    template_name = "core/cluster_confirm_delete.html"
    success_url = reverse_lazy("cluster_list")



# Variety CRUD

class VarietyCreateView(LoginRequiredMixin, CreateView):
    model = Variety
    fields = ["name", "harvest_start", "qr_prefix", "fruit_type"]
    template_name = "core/variety_form.html"
    success_url = reverse_lazy("variety_list")

class VarietyUpdateView(LoginRequiredMixin, UpdateView):
    model = Variety
    fields = ["name", "harvest_start", "qr_prefix", "fruit_type"]
    template_name = "core/variety_form.html"
    success_url = reverse_lazy("variety_list")

class VarietyDeleteView(LoginRequiredMixin, DeleteView):
    model = Variety
    template_name = "core/variety_confirm_delete.html"
    success_url = reverse_lazy("variety_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError as e:
            messages.error(request,
                "この品種はまだ圃場から参照されているため、削除できません。"
            )
            return redirect(self.success_url)

# Field CRUD
class FieldListView(LoginRequiredMixin, TemplateView):
    template_name = "core/field_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 🍑 桃の圃場 → variety の果実種別を使う場合
        ctx["peach_fields"] = Field.objects.filter(
            variety__fruit_type="peach"
        ).select_related("variety").order_by("name")
        # 🍇 ぶどうの圃場
        ctx["grape_fields"] = Field.objects.filter(
            variety__fruit_type="grape"
        ).select_related("variety").order_by("name")
        return ctx

class FieldCreateView(LoginRequiredMixin, CreateView):
    model = Field
    fields = ["name", "address", "area", "variety", "tree_count", "qr_suggestion"]
    template_name = "core/field_form.html"
    success_url = reverse_lazy("field_list")

class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = Field
    fields = ["name", "address", "area", "variety", "tree_count", "qr_suggestion"]
    template_name = "core/field_form.html"
    success_url = reverse_lazy("field_list")

class FieldDeleteView(LoginRequiredMixin, DeleteView):
    model = Field
    template_name = "core/field_confirm_delete.html"
    success_url = reverse_lazy("field_list")

# TaskType CRUD
class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "core/tasktype_list.html"
    context_object_name = "tasktypes"

class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = ["name"]
    template_name = "core/tasktype_form.html"
    success_url = reverse_lazy("tasktype_list")

class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = ["name"]
    template_name = "core/tasktype_form.html"
    success_url = reverse_lazy("tasktype_list")

class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    template_name = "core/tasktype_confirm_delete.html"
    success_url = reverse_lazy("tasktype_list")

# TaskSchedule CRUD
class TaskScheduleListView(LoginRequiredMixin, ListView):
    model = TaskSchedule
    template_name = "core/schedule_list.html"
    context_object_name = "schedules"

    def get_queryset(self):
        return TaskSchedule.objects.filter(variety_id=self.kwargs["variety_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variety = get_object_or_404(Variety, pk=self.kwargs["variety_id"])
        context["variety"] = variety
        return context

class TaskScheduleCreateView(LoginRequiredMixin, CreateView):
    model = TaskSchedule
    fields = ["seq", "task_type", "start_period", "end_period", "unit"]
    template_name = "core/schedule_form.html"

    def form_valid(self, form):
        form.instance.variety_id = self.kwargs["variety_id"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # ここで template に variety_id を渡す
        ctx = super().get_context_data(**kwargs)
        ctx["variety_id"] = self.kwargs["variety_id"]
        return ctx

    def get_success_url(self):
        return reverse_lazy("schedule_list", args=[self.kwargs["variety_id"]])


class TaskScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskSchedule
    fields = ["seq", "task_type", "start_period", "end_period", "unit"]
    template_name = "core/schedule_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 編集時は object.variety_id を渡す
        ctx["variety_id"] = self.object.variety_id
        return ctx

    def get_success_url(self):
        return reverse_lazy("schedule_list", args=[self.object.variety_id])

# core/views.py

class TaskScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskSchedule
    template_name = "core/schedule_confirm_delete.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # self.object は削除対象の TaskSchedule インスタンス
        ctx["variety_id"] = self.object.variety_id
        return ctx

    def get_success_url(self):
        return reverse_lazy("schedule_list", args=[self.object.variety_id])






# API: WorkStart
class WorkStartAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = WorkLogStartSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        worklog = ser.save()
        return Response({"id": worklog.id, "ok": True})

class WorkEndAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = WorkLogEndSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        worklog = ser.save()
        return Response({
            "id": worklog.id,
            "end_at": worklog.end_at,
            "ok": True
        })




class WorkLogListView(LoginRequiredMixin, ListView):
    model = WorkLog
    template_name = "core/worklog_list.html"
    context_object_name = "worklogs"

    def get_queryset(self):
        qs = WorkLog.objects.select_related("tree", "task_type", "user").all()

        self.form = WorkLogFilterForm(self.request.GET)

        if self.form.is_valid():
            if self.form.cleaned_data["user"]:
                qs = qs.filter(user=self.form.cleaned_data["user"])
            if self.form.cleaned_data["task_type"]:
                qs = qs.filter(task_type=self.form.cleaned_data["task_type"])
            if self.form.cleaned_data["date_from"]:
                qs = qs.filter(start_at__date__gte=self.form.cleaned_data["date_from"])
            if self.form.cleaned_data["date_to"]:
                qs = qs.filter(start_at__date__lte=self.form.cleaned_data["date_to"])
        return qs.order_by("-start_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form

        total_seconds = sum([
            (w.end_at - w.start_at).total_seconds()
            for w in self.object_list
            if w.end_at
        ])
        context["total_minutes"] = int(total_seconds // 60)
        context["count"] = self.object_list.count()
        return context



from .utils import get_lat_lon, get_weather
from .utils import try_address_with_backoff, get_weather

def field_weather_view(request, field_id):
    field = get_object_or_404(Field, pk=field_id)

    # 自動バックオフで住所調整しながら緯度経度を取得
    lat, lon = try_address_with_backoff(field.address)

    weather = None
    if lat and lon:
        weather = get_weather(lat, lon, "e3ff5a39a8d0f529705aa847a2fecdc7")

    return render(request, "core/field_weather.html", {
        "field": field,
        "weather": weather
    })




class AllSchedulesView(LoginRequiredMixin, TemplateView):
    template_name = "core/all_schedules.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["peaches"] = Variety.objects.filter(fruit_type="peach").order_by("name")
        ctx["grapes"]  = Variety.objects.filter(fruit_type="grape").order_by("name")
        return ctx



from django.views.generic import CreateView
from .models import Cluster, ClusterPhoto
from django.views.generic import CreateView
from .models import Cluster, ClusterPhoto
from .forms import ClusterPhotoForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
import base64

class ClusterPhotoCreateView(LoginRequiredMixin, CreateView):
    model = ClusterPhoto
    form_class = ClusterPhotoForm
    template_name = "core/clusterphoto_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cluster"] = get_object_or_404(Cluster, pk=self.kwargs["cluster_id"])
        return ctx

    def get_success_url(self):
        return reverse_lazy("cluster_detail", args=[self.kwargs["cluster_id"]])

    def form_valid(self, form):
        cluster = get_object_or_404(Cluster, pk=self.kwargs["cluster_id"])
        form.instance.cluster = cluster

        image_data = self.request.POST.get("image_data")
        print("📷 image_data present:", bool(image_data))
        print("📁 request.FILES['image']:", self.request.FILES.get("image"))

        if image_data and not self.request.FILES.get("image"):
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                file = ContentFile(base64.b64decode(imgstr),
                                   name=f"photo_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}")
                form.instance.image = file
                print("✅ image was decoded and assigned.")
            except Exception as e:
                print("❌ error decoding image:", e)
                form.add_error(None, "画像データの処理に失敗しました。")
                return self.form_invalid(form)
        else:
            print("⚠ image_data 条件不成立。base64もFILESもなし？")

        return super().form_valid(form)

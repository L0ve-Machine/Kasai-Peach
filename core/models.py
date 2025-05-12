from django.conf import settings
from django.db import models
from django.urls import reverse_lazy

class Variety(models.Model):
    name = models.CharField("品種名", max_length=100)
    harvest_start = models.CharField("収穫時期スタート", max_length=50, blank=True)
    qr_prefix = models.CharField("QR接頭辞", max_length=20, blank=True)

    FRUIT_CHOICES = [
        ("peach", "桃"),
        ("grape", "ぶどう"),
]
    fruit_type = models.CharField(
        "果実種別",
       max_length = 10,
        choices = FRUIT_CHOICES,
        default = "peach",
    )

    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField("圃場名", max_length=100)
    address = models.CharField("住所", max_length=200)
    area = models.PositiveIntegerField("面積(㎡)")
    variety = models.ForeignKey(Variety, on_delete=models.PROTECT, verbose_name="品種")
    tree_count = models.PositiveIntegerField("本数")
    qr_suggestion = models.CharField("畑QR提案", max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.variety.name})"

class TaskType(models.Model):
    name = models.CharField("作業種", max_length=50)

    def __str__(self):
        return self.name

class Tree(models.Model):
    qr_id = models.CharField("QRコードID", max_length=50, unique=True)
    variety = models.ForeignKey(
        Variety, on_delete=models.PROTECT, verbose_name="品種",
        null=True, blank=True
    )
    field = models.ForeignKey(
        Field, on_delete=models.PROTECT, verbose_name="圃場",
        null=True, blank=True
    )
    age = models.PositiveIntegerField("樹齢(年)", null=True, blank=True)
    planting_date = models.DateField("植付日", null=True, blank=True)
    transplant_date = models.DateField("定植日", null=True, blank=True)
    nursery = models.CharField("苗木業者", max_length=100, blank=True)
    training_type = models.CharField("仕立て方式", max_length=50, blank=True)

    def __str__(self):
        return self.qr_id

class WorkLog(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, verbose_name="樹木")
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT, verbose_name="作業種")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="実施者")
    start_at = models.DateTimeField("開始日時", auto_now_add=True)
    end_at = models.DateTimeField("終了日時", null=True, blank=True)

    def __str__(self):
        return f"{self.tree.qr_id} {self.task_type.name} {self.start_at:%Y-%m-%d %H:%M}"

class Cluster(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, verbose_name="樹木")
    number = models.CharField("房番号", max_length=30)
    created_at = models.DateTimeField("撮影日時(自動)", auto_now_add=True)

    def __str__(self):
        return f"{self.tree.qr_id} - {self.number}"

# 追加：作業スケジュール管理用モデル
class TaskSchedule(models.Model):
    variety = models.ForeignKey(
        Variety, on_delete=models.PROTECT, verbose_name="品種"
    )
    seq = models.PositiveIntegerField("番号")                     # ← 追加
    task_type = models.ForeignKey(
        TaskType, on_delete=models.PROTECT, verbose_name="作業種"
    )
    start_period = models.CharField("開始時期", max_length=20)
    end_period = models.CharField("終了時期", max_length=20, blank=True)
    unit = models.CharField("作業単位", max_length=10)

    class Meta:
        verbose_name = "作業スケジュール"
        verbose_name_plural = "作業スケジュール一覧"
        ordering = ["variety", "seq"]  # 番号順にソート

    def __str__(self):
        return f"{self.variety.name} #{self.seq} {self.task_type.name}"

    def get_absolute_url(self):
        # 編集後のリダイレクト先：一覧に戻る
        return reverse_lazy("schedule_list", args=[self.variety_id])
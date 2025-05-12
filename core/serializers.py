from rest_framework import serializers
from .models import WorkLog
from django.utils import timezone

class WorkLogStartSerializer(serializers.Serializer):
    qr_id = serializers.CharField()
    task_type_id = serializers.IntegerField()

    def create(self, validated):
        from .models import Tree, TaskType, WorkLog
        tree = Tree.objects.get(qr_id=validated["qr_id"])
        task = TaskType.objects.get(id=validated["task_type_id"])
        user = self.context["request"].user
        return WorkLog.objects.create(tree=tree, task_type=task, user=user)



class WorkLogEndSerializer(serializers.Serializer):
    worklog_id = serializers.IntegerField()

    def validate_worklog_id(self, value):
        try:
            worklog = WorkLog.objects.get(id=value)
        except WorkLog.DoesNotExist:
            raise serializers.ValidationError("WorkLog not found.")
        if worklog.end_at:
            raise serializers.ValidationError("This work is already ended.")
        return value

    def save(self):
        worklog = WorkLog.objects.get(id=self.validated_data["worklog_id"])
        worklog.end_at = timezone.now()
        worklog.save(update_fields=["end_at"])
        return worklog

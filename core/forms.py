from django import forms
from .models import TaskSchedule

class TaskScheduleForm(forms.ModelForm):
    class Meta:
        model = TaskSchedule
        fields = ["seq", "task_type", "start_period", "end_period", "unit"]
        widgets = {
            "seq": forms.NumberInput(attrs={"class": "form-control"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "start_period": forms.TextInput(attrs={"class": "form-control"}),
            "end_period": forms.TextInput(attrs={"class": "form-control"}),
            "unit": forms.TextInput(attrs={"class": "form-control"}),
        }


from .models import TaskType
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkLogFilterForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="作業者",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        label="作業種別",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    date_from = forms.DateField(
        required=False,
        label="開始日",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    date_to = forms.DateField(
        required=False,
        label="終了日",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
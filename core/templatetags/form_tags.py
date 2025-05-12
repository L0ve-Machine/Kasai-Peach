from django import template
register = template.Library()

@register.filter(name="add_class")
def add_class(field, css_class: str):
    """フォームフィールドに CSS クラスを追加する簡易フィルタ"""
    return field.as_widget(attrs={"class": css_class})

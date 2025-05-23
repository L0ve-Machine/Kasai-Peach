# Generated by Django 5.1.4 on 2025-04-26 02:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(auto_now_add=True)),
                ('end_at', models.DateTimeField(blank=True, null=True)),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tasktype')),
                ('tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tree')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

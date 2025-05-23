# Generated by Django 5.1.4 on 2025-04-28 08:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='圃場名')),
                ('address', models.CharField(max_length=200, verbose_name='住所')),
                ('area', models.PositiveIntegerField(verbose_name='面積（㎡）')),
                ('tree_count', models.PositiveIntegerField(verbose_name='本数')),
                ('qr_suggestion', models.CharField(blank=True, max_length=20, verbose_name='畑QRコード提案')),
            ],
        ),
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='品種名')),
                ('harvest_start', models.CharField(blank=True, max_length=50, verbose_name='収穫時期スタート')),
                ('qr_prefix', models.CharField(blank=True, max_length=20, verbose_name='QR接頭辞')),
            ],
        ),
        migrations.AddField(
            model_name='tree',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='樹齢(年)'),
        ),
        migrations.AddField(
            model_name='tree',
            name='nursery',
            field=models.CharField(blank=True, max_length=100, verbose_name='苗木仕入れ先'),
        ),
        migrations.AddField(
            model_name='tree',
            name='planting_date',
            field=models.DateField(blank=True, null=True, verbose_name='植付日'),
        ),
        migrations.AddField(
            model_name='tree',
            name='training_type',
            field=models.CharField(blank=True, max_length=50, verbose_name='仕立て方式'),
        ),
        migrations.AddField(
            model_name='tree',
            name='transplant_date',
            field=models.DateField(blank=True, null=True, verbose_name='定植日'),
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='name',
            field=models.CharField(max_length=50, verbose_name='作業種'),
        ),
        migrations.AlterField(
            model_name='tree',
            name='qr_id',
            field=models.CharField(max_length=50, unique=True, verbose_name='QRコードID'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='end_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='終了日時'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='start_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='開始日時'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tasktype', verbose_name='作業種'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='tree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tree', verbose_name='樹木'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='実施者'),
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30, verbose_name='房番号')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='撮影日時(自動)')),
                ('tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tree', verbose_name='樹木')),
            ],
        ),
        migrations.AddField(
            model_name='tree',
            name='field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.field', verbose_name='圃場'),
        ),
        migrations.AddField(
            model_name='field',
            name='variety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.variety', verbose_name='品種'),
        ),
        migrations.AddField(
            model_name='tree',
            name='variety',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.variety', verbose_name='品種'),
        ),
    ]

# Generated by Django 3.2.8 on 2022-02-28 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0002_auto_20220221_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadmapcontents',
            name='content',
            field=models.CharField(max_length=50, unique=True, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='roadmaptitles',
            name='title',
            field=models.CharField(max_length=30, unique=True, verbose_name='タイトル'),
        ),
    ]
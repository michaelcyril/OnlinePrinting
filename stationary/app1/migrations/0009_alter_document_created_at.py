# Generated by Django 4.0.4 on 2023-01-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_rename_staionery_id_document_stationery_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
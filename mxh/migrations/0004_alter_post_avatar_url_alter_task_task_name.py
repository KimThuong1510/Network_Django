# Generated by Django 4.2.8 on 2025-05-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mxh', '0003_task_deadline_task_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='avatar_url',
            field=models.ImageField(blank=True, null=True, upload_to='posts/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]

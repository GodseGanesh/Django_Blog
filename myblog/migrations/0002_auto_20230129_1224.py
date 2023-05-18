# Generated by Django 3.2.8 on 2023-01-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=70, null=True),
        ),
    ]

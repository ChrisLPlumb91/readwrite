# Generated by Django 4.1.6 on 2023-03-04 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletinboard', '0005_comment_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulletin',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
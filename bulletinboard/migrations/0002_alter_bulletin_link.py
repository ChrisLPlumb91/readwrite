# Generated by Django 4.1.6 on 2023-02-14 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletinboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='link',
            field=models.URLField(),
        ),
    ]
# Generated by Django 3.0.1 on 2020-01-18 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20200117_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='remark',
            field=models.TextField(blank=True),
        ),
    ]

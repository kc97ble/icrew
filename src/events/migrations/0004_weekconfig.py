# Generated by Django 3.0.1 on 2020-01-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200103_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeekConfig',
            fields=[
                ('week_no', models.IntegerField(primary_key=True, serialize=False)),
                ('reg_start_at', models.DateTimeField(null=True)),
                ('reg_ended_at', models.DateTimeField(null=True)),
            ],
        ),
    ]

# Generated by Django 2.2.16 on 2022-06-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schedule", "0004_schedule_scheduling"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="err",
            field=models.TextField(default="", verbose_name="schedule error message"),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.8 on 2024-02-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("predictor", "0005_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="medicalspecialistprofile",
            name="specialis_area",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
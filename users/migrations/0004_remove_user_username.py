# Generated by Django 5.0.6 on 2024-07-18 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_payment_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
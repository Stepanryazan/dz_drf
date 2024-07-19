from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0006_subscription_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="status",
            field=models.BooleanField(
                blank=True, default=True, null=True, verbose_name="Cтатус подписки"
            ),
        ),
    ]
# Generated by Django 4.2.7 on 2024-02-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("musicalapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lista",
            name="subtotal",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

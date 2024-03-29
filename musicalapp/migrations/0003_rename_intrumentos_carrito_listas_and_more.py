# Generated by Django 4.2.7 on 2024-03-04 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("musicalapp", "0002_alter_lista_subtotal"),
    ]

    operations = [
        migrations.RenameField(
            model_name="carrito",
            old_name="intrumentos",
            new_name="listas",
        ),
        migrations.AlterField(
            model_name="carrito",
            name="comprador",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="musicalapp.comprador"
            ),
        ),
        migrations.AlterField(
            model_name="lista",
            name="subtotal",
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-24 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_exchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharepart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='party.spareitem'),
        ),
    ]

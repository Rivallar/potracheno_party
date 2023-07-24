# Generated by Django 4.2.3 on 2023-07-21 11:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0002_alter_party_options_party_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gives', to='party.member')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges', to='party.party')),
                ('taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='takes', to='party.member')),
            ],
        ),
    ]

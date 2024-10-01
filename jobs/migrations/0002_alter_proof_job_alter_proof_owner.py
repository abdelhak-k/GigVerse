# Generated by Django 5.0.7 on 2024-09-17 15:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proof',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proofs', to='jobs.job'),
        ),
        migrations.AlterField(
            model_name='proof',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proofs', to=settings.AUTH_USER_MODEL),
        ),
    ]

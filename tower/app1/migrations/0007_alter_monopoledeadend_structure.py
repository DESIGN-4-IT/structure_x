# Generated by Django 5.1.2 on 2025-04-28 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_listofstructure_structure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monopoledeadend',
            name='structure',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='monopole_deadends', to='app1.listofstructure'),
        ),
    ]

# Generated by Django 5.1.2 on 2025-06-14 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_uploadedfile4'),
    ]

    operations = [
        migrations.CreateModel(
            name='TowerDeadend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_3_phase_circuits', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('num_shield_wires', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('num_1_phase_circuits', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('num_communication_cables', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tower_deadends', to='app1.listofstructure', unique=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('structure',), name='unique_tower_per_structure')],
            },
        ),
        migrations.CreateModel(
            name='tUploadedFile1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tuploaded_files1', to='app1.listofstructure')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('structure',), name='tunique_file_per_structure1')],
            },
        ),
    ]

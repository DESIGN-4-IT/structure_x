# Generated by Django 5.1.2 on 2025-06-16 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_hdeadend1_huploadedfile1'),
    ]

    operations = [
        migrations.CreateModel(
            name='HDeadend2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_3_phase_circuits', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('num_shield_wires', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('num_1_phase_circuits', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('num_communication_cables', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='h_deadends2', to='app1.listofstructure', unique=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('structure',), name='unique_h_per_structure2')],
            },
        ),
        migrations.CreateModel(
            name='hUploadedFile2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='huploaded_files2', to='app1.listofstructure')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('structure',), name='hunique_file_per_structure2')],
            },
        ),
    ]

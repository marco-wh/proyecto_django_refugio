# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2025-01-21 21:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_mascotas', models.IntegerField()),
                ('razones', models.TextField()),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adopcion.Persona')),
            ],
        ),
    ]

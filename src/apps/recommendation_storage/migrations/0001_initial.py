# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 07:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenreBasedTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LibraryBasedTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RedisConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=150)),
                ('port', models.PositiveIntegerField()),
                ('db', models.PositiveIntegerField()),
                ('busy', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TagBasedTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recommendation_storage.RedisConnection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrackBasedTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recommendation_storage.RedisConnection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='librarybasedtable',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recommendation_storage.RedisConnection'),
        ),
        migrations.AddField(
            model_name='genrebasedtable',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recommendation_storage.RedisConnection'),
        ),
    ]

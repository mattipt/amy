# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-13 01:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0114_instructor_training_workflow'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sponsorship',
            unique_together=set([('organization', 'event', 'amount')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-26 13:06
# Updated in Django 2.0.5 on 2018-06-02 11:15
from __future__ import unicode_literals

import json

from django.db import migrations, models


PREVIOUS_NAME_MAX_LENGTH = 40


def fix_truncated_language_names(apps, schema_editor):
    """Some languages names were truncated in 0097_auto_20160519_0739 migration.

    See https://github.com/swcarpentry/amy/issues/1165 for more info."""

    Language = apps.get_model('workshops', 'Language')

    # read list of languages
    languages_json = json.load(open('data/registry.json', encoding='utf-8'))
    # 1. (most inner) filter out non-language (sublanguages, dialects etc.)
    # 2. (middle) apply ' '.join(language['Description']) and therefore make it
    #    a list of descriptions
    # 3. (top) filter out shorter language names
    long_names = filter(
        lambda x: len(x) >= PREVIOUS_NAME_MAX_LENGTH,
        map(
            lambda y: ' '.join(y['Description']),
            filter(
                lambda z: z['Type'] == 'language' and len(z['Subtag']) <= 2,
                languages_json
            )
        )
    )

    for language_name in long_names:
        truncated = language_name[:PREVIOUS_NAME_MAX_LENGTH]
        try:
            lang = Language.objects.get(name=truncated)
        except Language.DoesNotExist:
            pass
        else:
            lang.name = language_name
            lang.save()


class Migration(migrations.Migration):
    dependencies = [
        ('workshops', '0138_auto_20180524_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text='Description of this language tag in English', max_length=100),
        ),
        migrations.RunPython(fix_truncated_language_names),
    ]

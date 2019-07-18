# Generated by Django 2.1.7 on 2019-07-18 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0186_extend_Curriculum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshoprequest',
            old_name='preferred_dates',
            new_name='other_preferred_dates',
        ),
        migrations.RenameField(
            model_name='workshoprequest',
            old_name='waiver_circumstances',
            new_name='scholarship_circumstances',
        ),
        migrations.RenameField(
            model_name='workshoprequest',
            old_name='centrally_organized_fee',
            new_name='administrative_fee',
        ),
        migrations.RenameField(
            model_name='workshoprequest',
            old_name='institution_name',
            new_name='institution_other_name',
        ),
    ]

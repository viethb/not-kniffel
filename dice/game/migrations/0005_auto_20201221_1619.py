# Generated by Django 3.1.4 on 2020-12-21 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20201221_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='max_score',
            new_name='score',
        ),
    ]

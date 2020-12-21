# Generated by Django 3.1.4 on 2020-12-21 16:31

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20201221_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_sheet', jsonfield.fields.JSONField(default=dict)),
                ('dice', jsonfield.fields.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.user')),
            ],
        ),
    ]

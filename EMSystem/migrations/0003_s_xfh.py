# Generated by Django 2.1 on 2021-02-14 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMSystem', '0002_s_jj'),
    ]

    operations = [
        migrations.AddField(
            model_name='s',
            name='xfh',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

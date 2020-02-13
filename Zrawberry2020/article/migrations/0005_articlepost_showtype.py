# Generated by Django 3.0.3 on 2020-02-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_articlepost_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='showtype',
            field=models.CharField(choices=[(0, 'DEFAULT'), (1, 'SPECIAL')], default='DEFAULT', max_length=10),
        ),
    ]
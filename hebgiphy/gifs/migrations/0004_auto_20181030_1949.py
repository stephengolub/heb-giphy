# Generated by Django 2.1.2 on 2018-10-30 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifs', '0003_auto_20181030_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gif',
            old_name='giphy_tags',
            new_name='tags',
        ),
    ]

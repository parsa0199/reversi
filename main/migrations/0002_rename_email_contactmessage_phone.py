# Generated by Django 4.1.7 on 2024-02-10 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='email',
            new_name='phone',
        ),
    ]

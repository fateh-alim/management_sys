# Generated by Django 4.2.5 on 2023-09-14 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock',
            new_name='Products',
        ),
    ]

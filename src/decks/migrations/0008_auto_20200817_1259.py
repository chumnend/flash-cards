# Generated by Django 3.0.8 on 2020-08-17 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0007_auto_20200804_2018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'categories'},
        ),
    ]

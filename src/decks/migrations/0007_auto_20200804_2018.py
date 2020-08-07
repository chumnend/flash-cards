# Generated by Django 3.0.8 on 2020-08-04 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0006_auto_20200804_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='publish_status',
            field=models.CharField(choices=[('x', 'Private'), ('f', 'Followers Only'), ('o', 'Everyone')], default='x', max_length=1),
        ),
    ]
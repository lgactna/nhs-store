# Generated by Django 3.1.6 on 2021-02-18 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210216_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='custom_links',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
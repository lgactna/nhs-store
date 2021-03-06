# Generated by Django 3.1.6 on 2021-02-18 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_order_custom_links'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='custom_links',
        ),
        migrations.AddField(
            model_name='order',
            name='custom_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.material'),
        ),
        migrations.AddField(
            model_name='order',
            name='custom_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_custom',
            field=models.BooleanField(default=False),
        ),
    ]

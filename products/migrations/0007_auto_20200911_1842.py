# Generated by Django 3.1 on 2020-09-11 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200911_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.URLField(default='https://via.placeholder.com/300x400?text=No+photo', max_length=2000),
        ),
    ]

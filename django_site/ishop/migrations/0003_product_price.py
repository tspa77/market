# Generated by Django 2.0.2 on 2018-02-22 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ishop', '0002_auto_20180222_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

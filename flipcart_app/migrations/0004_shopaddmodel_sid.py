# Generated by Django 4.1.4 on 2023-01-29 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flipcart_app', '0003_shopaddmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopaddmodel',
            name='sid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
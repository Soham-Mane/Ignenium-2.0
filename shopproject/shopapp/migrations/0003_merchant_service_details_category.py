# Generated by Django 4.2.1 on 2023-09-14 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0002_remove_merchant_service_details_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_service_details',
            name='category',
            field=models.CharField(default='health', max_length=50),
        ),
    ]
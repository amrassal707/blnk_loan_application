# Generated by Django 5.0.1 on 2024-01-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_loanapplication_amount_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='fully_paid',
            field=models.BooleanField(default=False),
        ),
    ]

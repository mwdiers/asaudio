# Generated by Django 4.0.2 on 2022-03-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0003_software_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='free',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
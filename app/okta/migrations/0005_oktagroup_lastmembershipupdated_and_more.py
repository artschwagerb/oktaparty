# Generated by Django 4.0.2 on 2022-08-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('okta', '0004_alter_oktagroup_options_alter_oktauser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='oktagroup',
            name='lastMembershipUpdated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='oktagroup',
            name='lastUpdated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

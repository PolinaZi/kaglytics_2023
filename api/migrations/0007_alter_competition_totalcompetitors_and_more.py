# Generated by Django 4.1.5 on 2023-03-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_competitions_data_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='totalCompetitors',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='totalSubmissions',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

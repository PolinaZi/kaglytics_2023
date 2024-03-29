# Generated by Django 4.1.5 on 2023-03-15 19:49
import pandas as pd
from django.db import migrations

from api.models import Tag


def add_tags(apps, schema_editor):
    df_tags = pd.read_csv("api/data/Tags.csv")
    for index, row in df_tags.iterrows():
        new_tag = Tag(kaggle_id=row['Id'], name=row['Name'])
        new_tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_competition_kaggle_id_organization_kaggle_id_and_more'),
    ]

    operations = [
        migrations.RunPython(add_tags),
    ]

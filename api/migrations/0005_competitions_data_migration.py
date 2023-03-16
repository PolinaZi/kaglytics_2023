# Generated by Django 4.1.5 on 2023-03-15 19:49
import pandas as pd
import logging
import math

from django.db import migrations
from datetime import datetime

from api.models import RewardType, Category, EvaluationMetric, Competition, Organization, Tag


def add_comp_categories(apps, schema_editor):
    df_competitions = pd.read_csv("api/data/out.csv", low_memory=False)
    comp_categories = set(df_competitions['HostSegmentTitle'])
    reward_types = set(df_competitions['RewardType'])
    evaluation_metrics = set(df_competitions['EvaluationAlgorithmName'])

    for rt in reward_types:
        new_reward_type = RewardType(name=rt)
        new_reward_type.save()

    for cc in comp_categories:
        new_comp_category = Category(name=cc)
        new_comp_category.save()

    for em in evaluation_metrics:
        new_eval_metric = EvaluationMetric(name=em)
        new_eval_metric.save()

    tag_names = list(df_competitions.columns.values)
    tag_names = tag_names[42:]

    for index, row in df_competitions.iterrows():
        try:
            enabled_date_object = datetime.strptime(row['EnabledDate'], '%m/%d/%Y %H:%M:%S')
            formatted_enabled_date = enabled_date_object.strftime('%Y-%m-%d %H:%M:%S')
            deadline_date_object = datetime.strptime(row['DeadlineDate'], '%m/%d/%Y %H:%M:%S')
            formatted_deadline_date = deadline_date_object.strftime('%Y-%m-%d %H:%M:%S')

            organization = None
            if str(row['OrganizationName']) != "nan":
                organization = Organization.objects.get(name=row['OrganizationName'])

            new_competition = Competition(title=row['Title'],
                                          description=row['Subtitle'],
                                          category=Category.objects.get(name=row['HostSegmentTitle']),
                                          organization=organization,
                                          evaluationMetric=EvaluationMetric.objects.get(name=row['EvaluationAlgorithmName']),
                                          maxDailySubmissions=int(row['MaxDailySubmissions']),
                                          maxTeamSize=int(row['MaxTeamSize']),
                                          rewardType=RewardType.objects.get(name=row['RewardType']),
                                          rewardQuantity=int(row['RewardQuantity']) if not math.isnan(row['RewardQuantity']) else 0,
                                          totalTeams=int(row['TotalTeams']),
                                          totalCompetitors=int(row['TotalCompetitors']),
                                          totalSubmissions=int(row['TotalSubmissions']),
                                          enabledDate=formatted_enabled_date,
                                          deadline=formatted_deadline_date)
            new_competition.save()

            competition_tags = list()
            for tag in tag_names:
                if row[tag] == 1:
                    competition_tags.append(Tag.objects.get(name=tag))
            new_competition.tags.set(competition_tags)

        except (Organization.DoesNotExist, Category.DoesNotExist, EvaluationMetric.DoesNotExist, Tag.DoesNotExist) as ex:
            logging.debug(ex)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_organizations_data_migration'),
    ]

    operations = [
        migrations.RunPython(add_comp_categories),
    ]

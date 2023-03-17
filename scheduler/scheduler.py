import os
import sys
import zipfile
from datetime import datetime

import numpy as np
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from api.kaggle_api import api
from api.models import Competition
from api.utils import extract_competition_from_row


def update_competitions_info_file():
    print("Start updating competitions info file...")
    for files in os.walk("./api/data"):
        if "Competitions.csv.zip" not in files:
            api.dataset_download_file('Kaggle/meta-kaggle', 'Competitions.csv', path="./api/data")
            with zipfile.ZipFile("./api/data/Competitions.csv.zip", 'r') as zip_ref:
                zip_ref.extractall("./api/data")
        if 'CompetitionTags.csv' not in files:
            api.dataset_download_file('Kaggle/meta-kaggle', 'CompetitionTags.csv', path="./api/data")

    df_competitions = pd.read_csv("./api/data/Competitions.csv")
    df_competitions_tags = pd.read_csv("./api/data/CompetitionTags.csv")
    df_tags = pd.read_csv("./api/data/Tags.csv")
    df_organizations = pd.read_csv("./api/data/Organizations.csv")

    tags_columns = set(df_competitions_tags['TagId'])
    for index, row in df_competitions_tags.iterrows():
        df_competitions.loc[df_competitions['Id'] == row['CompetitionId'], str(row['TagId'])] = 1

    for tag in tags_columns:
        df_competitions[str(tag)] = np.where(df_competitions[str(tag)] != 1, 0, 1)

    for index, row in df_tags.iterrows():
        df_competitions = df_competitions.rename(columns={str(row['Id']): row['Name']})

    df_competitions['OrganizationId'] = df_competitions['OrganizationId'].astype(str)
    for index, row in df_organizations.iterrows():
        df_competitions.loc[df_competitions['OrganizationId'] == str(float(row['Id'])), 'OrganizationId'] = row['Name']

    df_competitions = df_competitions.rename(columns={'OrganizationId': 'OrganizationName'})
    df_competitions.to_csv("./api/data/out.csv", sep=',', encoding='utf-8', index=False)
    print("Competitions info file updated successfully.")


def update_competitions_info_table():
    print("Start updating competitions info table...")
    df_competitions = pd.read_csv("api/data/out.csv", low_memory=False)
    for index, row in df_competitions.iterrows():
        deadline_date_object = datetime.strptime(row['DeadlineDate'], '%m/%d/%Y %H:%M:%S')
        if deadline_date_object.year == datetime.now().year:
            new_competition = extract_competition_from_row(row)
            try:
                competition = Competition.objects.get(title=new_competition.title)
                competition = new_competition
                new_competition.id = competition.id
                new_competition.save()
            except Competition.DoesNotExist as e:
                new_competition.save()
        else:
            continue
    print("Competitions info table updated successfully.")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(update_competitions_info_file, 'interval', hours=24, name='update_competitions_info_file',
                      jobstore='default')
    scheduler.add_job(update_competitions_info_table, 'interval', hours=24, name='update_competitions_info_table',
                      jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)

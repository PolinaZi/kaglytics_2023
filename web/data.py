import os
import zipfile
import numpy as np
import pandas as pd

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

competitions_data_files = api.dataset_list_files('Kaggle/meta-kaggle').files
print("-- Dataset files: --")
for f in range(len(competitions_data_files)):
    print(competitions_data_files[f])

for files in os.walk("data"):
    if "Competitions.csv.zip" not in files:
        api.dataset_download_file('Kaggle/meta-kaggle', 'Competitions.csv', path="data")
        with zipfile.ZipFile("data/Competitions.csv.zip", 'r') as zip_ref:
            zip_ref.extractall("data")
    if 'CompetitionTags.csv' not in files:
        api.dataset_download_file('Kaggle/meta-kaggle', 'CompetitionTags.csv', path="data")
    # if 'Organizations.csv' not in files:
    #     api.dataset_download_file('Kaggle/meta-kaggle', 'Organizations.csv', path="data")
    # if 'Tags.csv' not in files:
    #     api.dataset_download_file('Kaggle/meta-kaggle', 'Tags.csv', path="data")

df_competitions = pd.read_csv("data/Competitions.csv")
df_competitions_tags = pd.read_csv("data/CompetitionTags.csv")
df_tags = pd.read_csv("data/Tags.csv")
df_organizations = pd.read_csv("data/Organizations.csv")

tags_columns = set(df_competitions_tags['TagId'])
# df_competitions = df_competitions.reindex(columns=df_competitions.columns.tolist() + list(tags_columns))

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
df_competitions.to_csv("data/out.csv", sep='\t', encoding='utf-8')

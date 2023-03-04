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
    # if 'Tags.csv' not in files:
    #     api.dataset_download_file('Kaggle/meta-kaggle', file_name="Tags.csv", path="data")

df_competitions = pd.read_csv("data/Competitions.csv")
df_competitions_tags = pd.read_csv("data/CompetitionTags.csv")

tags_columns = set(df_competitions_tags['TagId'])

for index, row in df_competitions_tags.iterrows():
    df_competitions.loc[df_competitions['Id'] == row['CompetitionId'], str(row['TagId'])] = 1

for tag in tags_columns:
    df_competitions[str(tag)] = np.where(df_competitions[str(tag)] != 1, 0, 1)

df_competitions.to_csv("data/competitions_data.csv", sep='\t', encoding='utf-8')

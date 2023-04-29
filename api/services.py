from api.kaggle_api import api
from .models import Tag
from .utils import extract_active_competition_from_row
import pandas as pd
import re


def get_active_competitions():
    api_competitions = api.competitions_list()
    return api_competitions


def active_competitions_to_list(df_competitions):
    competitions = []

    for index, row in df_competitions.iterrows():
        new_competition = extract_active_competition_from_row(row)
        competitions.append(new_competition)

    return competitions


def active_competitions_to_df():
    api_competitions = get_active_competitions()
    comp_list = []
    for c in api_competitions:
        comp_list.append(vars(c))

    feature_names = ['category', 'deadline', 'description', 'enabledDate', 'evaluationMetric', 'maxDailySubmissions',
                     'maxTeamSize', 'organizationName', 'reward', 'tags', 'title', 'id']

    active_df = pd.DataFrame(comp_list, columns=feature_names)
    active_df.columns = map(str.lower, active_df.columns)

    reward_type = []
    reward_quantity = []
    for index, row in active_df.iterrows():

        if re.match(r'(\$)', row['reward']):
            s = re.match(r'(?:\$)(.+)', row['reward']).group(1).replace(',', '')
            reward_type.append('USD')
            reward_quantity.append(int(s))

        elif re.match(r'(\€)', row['reward']):
            s = re.match(r'(?:€)(.+)', row['reward']).group(1).replace(',', '')
            reward_type.append('EUR')
            reward_quantity.append(int(s))

        else:
            reward_type.append(row['reward'])
            reward_quantity.append(0)

    active_df['rewardtype'] = reward_type
    active_df['rewardquantity'] = reward_quantity

    tags_names = map(lambda t: t.name, Tag.objects.all())

    for tag in tags_names:
        tag_list = []
        for index, row in active_df.iterrows():
            row['tags'] = map(lambda t: str(t), row['tags'])
            tag_list.append(1 if tag in row['tags'] else 0)
        active_df[tag] = tag_list

    active_df.drop(columns=['tags', 'reward'], inplace=True)
    return active_df


def get_filtered_active_competitions(title=None, category=None, reward_type=None, deadline_before=None,
                                     deadline_after=None, tags=None):
    competitions = api.competitions_list()

    if title is not None:
        competitions = [c for c in competitions if title.lower() in c.title.lower()]
    if category is not None:
        competitions = [c for c in competitions if category == c.category]
    if reward_type is not None:
        competitions = [c for c in competitions if reward_type == c.reward]
    if deadline_before is not None:
        competitions = [c for c in competitions if deadline_before >= c.deadline]
    if deadline_after is not None:
        competitions = [c for c in competitions if deadline_after <= c.deadline]
    if tags is not None:
        competitions = [c for c in competitions if
                        all(tag.lower() in map(lambda t: t.name.lower(), c.tags) for tag in tags)]

    return competitions

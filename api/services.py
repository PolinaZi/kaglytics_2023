import re

import pandas as pd

from api.kaggle_api import api
from .dto import TagDto
from .models import Tag
from .utils import extract_active_competition_from_row


def get_active_competitions():
    api_competitions = api.competitions_list()
    return api_competitions


def get_filtered_active_competitions(title=None, category=None, reward_type=None, deadline_before=None,
                                     deadline_after=None, tags=None):
    competitions = api.competitions_list()

    if title is not None:
        competitions = [c for c in competitions if title.lower() in c.title.lower()]
    if category is not None:
        competitions = [c for c in competitions if category.lower() == c.category.lower()]
    if reward_type is not None:
        competitions = [c for c in competitions if reward_type.lower() == c.reward.lower()]
    if deadline_before is not None:
        competitions = [c for c in competitions if deadline_before >= c.deadline]
    if deadline_after is not None:
        competitions = [c for c in competitions if deadline_after <= c.deadline]
    if tags is not None:
        competitions = [c for c in competitions if
                        all(tag.lower() in map(lambda t: t.name.lower(), c.tags) for tag in tags)]

    return competitions


def active_competitions_to_dto_list(df_competitions):
    competitions = []

    tag_names = list(df_competitions.columns.values)
    tag_names = tag_names[14:]

    for index, row in df_competitions.iterrows():
        new_competition_dto = extract_active_competition_from_row(row).to_dto()

        competition_tags = list()
        for tag in tag_names:
            if row[tag] == 1:
                try:
                    c_tag = Tag.objects.get(name=tag).to_dto()
                except Tag.DoesNotExist:
                    c_tag = TagDto(sid=0, kaggle_id=0, name=tag)
                competition_tags.append(c_tag)

        new_competition_dto.tags_dto = competition_tags
        competitions.append(new_competition_dto)

    return competitions


def api_competitions_to_df(competitions):
    api_competitions = competitions
    comp_list = []
    for c in api_competitions:
        comp_list.append(vars(c))

    feature_names = ['title', 'description', 'category', 'organizationname', 'evaluationmetric', 'maxdailysubmissions',
                     'maxteamsize', 'reward', 'deadline', 'enabledDate', 'tags', 'id', 'mergerDeadline',
                     'newEntrantDeadline']

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

    active_df.insert(loc=7, column='rewardtype', value=reward_type)
    active_df.insert(loc=8, column='rewardquantity', value=reward_quantity)

    tags_names = map(lambda t: t.name, Tag.objects.all())

    for tag in tags_names:
        tag_list = []
        for index, row in active_df.iterrows():
            row['tags'] = map(lambda t: str(t), row['tags'])
            tag_list.append(1 if tag in row['tags'] else 0)
        active_df[tag] = tag_list

    active_df.drop(columns=['tags', 'reward'], inplace=True)
    return active_df


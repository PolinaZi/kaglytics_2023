from api.kaggle_api import api


def get_active_competitions():
    api_competitions = api.competitions_list()
    return api_competitions


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
        competitions = [c for c in competitions if all(tag.lower() in map(lambda t: t.name.lower(), c.tags) for tag in tags)]

    return competitions

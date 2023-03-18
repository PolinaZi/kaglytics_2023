from api.models import Competition, Category, Organization, EvaluationMetric, RewardType
from api.kaggle_api import api


def get_active_competitions():
    competitions_list = []
    api_competitions = api.competitions_list()

    for comp in api_competitions:
        reward_type = None
        reward_quantity = 0.0
        organization = None
        evaluation_metric = None
        try:
            reward_type = RewardType.objects.get(name=comp.reward)
        except RewardType.DoesNotExist:
            reward_quantity = float(comp.reward[1:].replace(',', '.'))
        try:
            organization = Organization.objects.get(name=comp.organizationName)
        except Organization.DoesNotExist:
            pass
        try:
            evaluation_metric = EvaluationMetric.objects.get(name=comp.evaluationMetric)
        except EvaluationMetric.DoesNotExist:
            pass

        competitions_list.append(Competition(
            kaggle_id=comp.id,
            title=comp.title,
            description=comp.description,
            category=Category.objects.get(name=comp.category),
            organization=organization,
            evaluationMetric=evaluation_metric,
            maxDailySubmissions=comp.maxDailySubmissions,
            maxTeamSize=comp.maxTeamSize,
            rewardType=reward_type,
            rewardQuantity=reward_quantity,
            totalTeams=comp.teamCount,
            enabledDate=comp.enabledDate,
            deadline=comp.deadline
        ))

    return competitions_list

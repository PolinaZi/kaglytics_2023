import math
from datetime import datetime

from api.models import Organization, Competition, Category, EvaluationMetric, RewardType


def extract_competition_from_row(row):
    enabled_date_object = datetime.strptime(row['EnabledDate'], '%m/%d/%Y %H:%M:%S')
    formatted_enabled_date = enabled_date_object.strftime('%Y-%m-%d %H:%M:%S')
    deadline_date_object = datetime.strptime(row['DeadlineDate'], '%m/%d/%Y %H:%M:%S')
    formatted_deadline_date = deadline_date_object.strftime('%Y-%m-%d %H:%M:%S')

    organization = None
    if str(row['OrganizationName']) != "nan":
        organization = Organization.objects.get(name=row['OrganizationName'])

    new_competition = Competition(kaggle_id=row['Id'],
                                  title=row['Title'],
                                  description=row['Subtitle'],
                                  category=Category.objects.get(name=row['HostSegmentTitle']),
                                  organization=organization,
                                  evaluationMetric=EvaluationMetric.objects.get(name=row['EvaluationAlgorithmName']),
                                  maxDailySubmissions=int(row['MaxDailySubmissions']),
                                  maxTeamSize=int(row['MaxTeamSize']),
                                  rewardType=RewardType.objects.get(name=row['RewardType']),
                                  rewardQuantity=int(row['RewardQuantity']) if not math.isnan(
                                      row['RewardQuantity']) else 0,
                                  totalTeams=int(row['TotalTeams']),
                                  totalCompetitors=int(row['TotalCompetitors']),
                                  totalSubmissions=int(row['TotalSubmissions']),
                                  enabledDate=formatted_enabled_date,
                                  deadline=formatted_deadline_date)
    return new_competition

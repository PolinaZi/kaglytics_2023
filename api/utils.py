import math
import string
import random
from datetime import datetime
from django.core.mail import EmailMessage

from api.dto import CompetitionDto
from api.models import Organization, Competition, Category, EvaluationMetric, RewardType, Tag


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


def extract_active_competition_from_row(row):
    try:
        category = Category.objects.get(name=row['category'])
    except Category.DoesNotExist:
        category = Category(name=row['category'])
    try:
        organization = Organization.objects.get(name=row['organizationname'])
    except Organization.DoesNotExist:
        organization = Organization(name=row['organizationname'])
    try:
        evaluation_metric = EvaluationMetric.objects.get(name=row['evaluationmetric'])
    except EvaluationMetric.DoesNotExist:
        evaluation_metric = EvaluationMetric(name=row['evaluationmetric'])
    try:
        reward_type = RewardType.objects.get(name=row['rewardtype'])
    except RewardType.DoesNotExist:
        reward_type = RewardType(name=row['rewardtype'])
    return Competition(kaggle_id=row['id'],
                       title=row['title'],
                       description=row['description'],
                       category=category,
                       organization=organization,
                       evaluationMetric=evaluation_metric,
                       maxDailySubmissions=int(row['maxdailysubmissions']),
                       maxTeamSize=int(row['maxteamsize']),
                       rewardType=reward_type,
                       rewardQuantity=int(row['rewardquantity']),
                       enabledDate=row['enableddate'],
                       deadline=row['deadline'])


# todo
# def ext(df_competitions):
#     competitions = []
#     tag_names = list(df_competitions.columns.values)
#     tag_names = tag_names[42:]
#
#     for index, row in df_competitions.iterrows():
#         try:
#             new_competition = extract_competition_from_row(row)
#             new_competition.save()
#
#             competition_tags = list()
#             for tag in tag_names:
#                 if row[tag] == 1:
#                     competition_tags.append(Tag.objects.get(name=tag))
#             new_competition.tags.set(competition_tags)


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
            from_email='leisanahmetova02@mail.ru'
        )
        email.send()


def generate_code():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(50))

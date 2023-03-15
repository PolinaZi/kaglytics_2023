import pandas as pd

deleted_columns = ['Id', 'Slug', 'ForumId', 'CompetitionTypeId', 'TeamModelDeadlineDate', 'ModelSubmissionDeadlineDate',
                   'FinalLeaderboardHasBeenVerified', 'HasKernels', 'OnlyAllowKernelSubmissions', 'HasLeaderboard',
                   'LeaderboardPercentage', 'LeaderboardDisplayFormat', 'EvaluationAlgorithmAbbreviation',
                   'EvaluationAlgorithmDescription', 'EvaluationAlgorithmIsMax', 'NumScoredSubmissions',
                   'BanTeamMergers', 'EnableTeamModels', 'NumPrizes', 'UserRankMultiplier', 'CanQualifyTiers',
                   'ValidationSetName', 'ValidationSetValue', 'EnableSubmissionModelHashes',
                   'EnableSubmissionModelAttachments', 'HostName', 'TotalTeams', 'TotalSubmissions']

renamed_columns = {'Subtitle': 'description', 'HostSegmentTitle': 'category', 'DeadlineDate': 'deadline',
                   'ProhibitNewEntrantsDeadlineDate': 'newEntrantDeadline', 'TeamMergerDeadlineDate': 'mergerDeadline',
                   'EvaluationAlgorithmName': 'evaluationMetric'}

cat_features = ['category', 'organizationname', 'evaluationmetric', 'rewardtype']
text_features = ['title', 'description']

datetime_format = '%m/%d/%Y %H:%M:%S'


def fill_string_na(df, features):
    for feature in features:
        df[feature].fillna('', inplace=True)


def create_new_features(df):
    df['duration'] = (df['deadline'] - df["enableddate"]).dt.days
    df['day_to_new'] = (df['deadline'] - df["newentrantdeadline"]).dt.days
    df['day_to_team'] = (df['deadline'] - df["mergerdeadline"]).dt.days

    df.drop(columns=['deadline', 'newentrantdeadline', 'mergerdeadline', 'enableddate'], inplace=True)


def preprocess_data(df):
    df.drop(columns=deleted_columns, inplace=True)

    df.rename(columns=renamed_columns, inplace=True)

    df.columns = map(str.lower, df.columns)

    df['enableddate'] = pd.to_datetime(df['enableddate'], format=datetime_format)
    df['deadline'] = pd.to_datetime(df['deadline'], format=datetime_format)
    df['newentrantdeadline'] = pd.to_datetime(df['newentrantdeadline'], format=datetime_format)
    df['mergerdeadline'] = pd.to_datetime(df['mergerdeadline'], format=datetime_format)

    create_new_features(df)

    df['day_to_new'].fillna(df.mode()['day_to_new'][0], inplace=True)
    df['day_to_team'].fillna(df.mode()['day_to_team'][0], inplace=True)

    df['rewardquantity'].fillna(0, inplace=True)

    fill_string_na(df, cat_features)
    fill_string_na(df, text_features)

    x = df.drop(['totalcompetitors'], axis=1)
    y = df['totalcompetitors']

    return x, y


data = pd.read_csv("data/out.csv", low_memory=False)
x, y = preprocess_data(data)

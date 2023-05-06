import pandas as pd

DELETED_COLUMNS = ['Id', 'Slug', 'ForumId', 'CompetitionTypeId', 'TeamModelDeadlineDate', 'ModelSubmissionDeadlineDate',
                   'FinalLeaderboardHasBeenVerified', 'HasKernels', 'OnlyAllowKernelSubmissions', 'HasLeaderboard',
                   'LeaderboardPercentage', 'LeaderboardDisplayFormat', 'EvaluationAlgorithmAbbreviation',
                   'EvaluationAlgorithmDescription', 'EvaluationAlgorithmIsMax', 'NumScoredSubmissions',
                   'BanTeamMergers', 'EnableTeamModels', 'NumPrizes', 'UserRankMultiplier', 'CanQualifyTiers',
                   'ValidationSetName', 'ValidationSetValue', 'EnableSubmissionModelHashes',
                   'EnableSubmissionModelAttachments', 'HostName', 'TotalTeams', 'TotalSubmissions']

RENAMED_COLUMNS = {'Subtitle': 'description', 'HostSegmentTitle': 'category', 'DeadlineDate': 'deadline',
                   'ProhibitNewEntrantsDeadlineDate': 'newEntrantDeadline', 'TeamMergerDeadlineDate': 'mergerDeadline',
                   'EvaluationAlgorithmName': 'evaluationMetric'}

CAT_FEATURES = ['category', 'organizationname', 'evaluationmetric', 'rewardtype']
TEXT_FEATURES = ['title', 'description']

DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'


def fill_string_na(df, features):
    for feature in features:
        df[feature].fillna('', inplace=True)


def create_new_features(df):
    df['duration'] = (df['deadline'] - df["enableddate"]).dt.days
    df['day_to_new'] = (df['deadline'] - df["newentrantdeadline"]).dt.days
    df['day_to_team'] = (df['deadline'] - df["mergerdeadline"]).dt.days

    df.drop(columns=['deadline', 'newentrantdeadline', 'mergerdeadline', 'enableddate'], inplace=True)


def preprocess_data(df):
    df.drop(columns=DELETED_COLUMNS, inplace=True)

    df.rename(columns=RENAMED_COLUMNS, inplace=True)

    df.columns = map(str.lower, df.columns)

    df['enableddate'] = pd.to_datetime(df['enableddate'], format=DATETIME_FORMAT)
    df['deadline'] = pd.to_datetime(df['deadline'], format=DATETIME_FORMAT)
    df['newentrantdeadline'] = pd.to_datetime(df['newentrantdeadline'], format=DATETIME_FORMAT)
    df['mergerdeadline'] = pd.to_datetime(df['mergerdeadline'], format=DATETIME_FORMAT)

    create_new_features(df)

    df['day_to_new'].fillna(df.mode()['day_to_new'][0], inplace=True)
    df['day_to_team'].fillna(df.mode()['day_to_team'][0], inplace=True)

    df['rewardquantity'].fillna(0, inplace=True)

    fill_string_na(df, CAT_FEATURES)
    fill_string_na(df, TEXT_FEATURES)

    x = df.drop(['totalcompetitors'], axis=1)
    y = df['totalcompetitors']

    return x, y

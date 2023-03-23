from catboost import Pool
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split


def split_data(x, y, test_size):
    return train_test_split(x, y, test_size=test_size, random_state=13)


def create_pools(x, y, test_size, cat_features, text_features):
    x_train, x_test, y_train, y_test = split_data(x, y, test_size)
    train_pool = Pool(
        x_train, y_train,
        cat_features=cat_features,
        text_features=text_features,
    )
    validation_pool = Pool(
        x_test, y_test,
        cat_features=cat_features,
        text_features=text_features,
    )
    return train_pool, validation_pool


def fit_model(train_pool, validation_pool, **kwargs):
    model = CatBoostRegressor(
        iterations=1000,
        learning_rate=0.05,
        **kwargs
    )

    return model.fit(
        train_pool,
        eval_set=validation_pool,
        verbose=100,
    )


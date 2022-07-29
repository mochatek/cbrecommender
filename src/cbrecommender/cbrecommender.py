from pandas import DataFrame, concat
from numpy import array
from .helpers import remove_spaces, ensure_type


class CBRecommender:
    """
    Class to represent Content-Based Recommender

    Attributes:
        user_profile (DatFrame): user's preference profile, based on which recommendation will be made
    """

    def __init__(self):
        """ Constructs all the necessary attributes for the recommender object. """
        self.user_profile = None

    @ensure_type([DataFrame], instance_method=True)
    def encode_features(self, features: DataFrame) -> DataFrame:
        """
        One-Hot-Encode the features used for recommendation

        Args:
            `features` (DataFrame): Features to encode
                Example: Movie genres

        Returns:
            `encoded_features` (DataFrame): One-Hot-Encoded form of the features
        """

        encoded_features = concat([features[feature_name].apply(
            remove_spaces).str.get_dummies(sep=',') for feature_name in features], axis=1)

        return encoded_features

    @ensure_type([DataFrame, list], instance_method=True)
    def fit(self, training_features: DataFrame, scores: list) -> DataFrame:
        """
        Builds the user_profile by extracting user's preference from the training_features and scores.

        Args:
            `training_features` (DataFrame): Features for training the model. It should be One-Hot-Encoded.
                Example: Genres of watched movies

            `scores` (float): Score associated to each item in training_features
                Example: User rating for each watched movie

        Returns:
            `user_profile` (DataFrame): The preference model built for the user, which will be used for recommending.
        """

        if len(training_features.index) != len(scores):
            raise ValueError(
                f'training_features and scores should be equal in length, got {len(training_features.index)} and {len(scores)} instead.')

        feature_matrix = training_features.values
        score_matrix = array(scores, ndmin=2)
        profile_matrix = score_matrix.dot(feature_matrix)
        normalized_profile_matrix = profile_matrix / profile_matrix.sum()

        self.user_profile = DataFrame(
            normalized_profile_matrix, columns=training_features.columns)
        return self.user_profile

    @ensure_type([DataFrame, DataFrame, float, int], instance_method=True)
    def recommend(self, items: DataFrame, test_features: DataFrame, threshold_score: float = 7.5, limit: int = -1) -> DataFrame:
        """
        Recommend items based on user_profile

        Args:
            `items` Items from which recommendation is needed

            `test_features` (DataFrame): One-Hot-Encoded features of the items.
                Example: Genres of unwatched movies

            `threshold_score` (float): Minimum score used as threshold value in recommending items. Default is 7.5

            `limit` (int): Number of items to recommend

        Returns:
            `recommendations` (DataFrame): DataFrame with item and predicted score.
        """

        if set(test_features.columns) != set(self.user_profile.columns):
            raise ValueError(
                f'test_feature columns should be same as that used in fit(). Expected {list(self.user_profile.columns)}, got {list(test_features.columns)} instead')

        items = items.squeeze()
        feature_matrix = test_features.values
        expected_scores = (
            feature_matrix * self.user_profile.values).sum(axis=1) * 10

        recommendations = DataFrame({
            'item': items,
            'expected score': expected_scores}).sort_values('expected score', ascending=False)
        return recommendations[recommendations['expected score'] >= threshold_score].iloc[:limit, :]

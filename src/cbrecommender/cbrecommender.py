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
        self.__user_profile = None

    @property
    def user_profile(self) -> DataFrame:
        """ Getter for user_profile """
        return self.__user_profile

    @staticmethod
    def clean_and_encode(features: DataFrame) -> DataFrame:
        """ Helper function to clean and One-Hot Encode the feature """
        return (features[feature_name].apply(
            remove_spaces).str.get_dummies(sep=',') for feature_name in features)

    @ensure_type([DataFrame], instance_method=True)
    def create_item_profile(self, features: DataFrame) -> DataFrame:
        """
        Creates a profile for every item based on the supplied features

        Args:
            `features` (DataFrame): Relevant attributes of the item, based on which the item profile is created
                Example: Movie genres

        Returns:
            `item_profiles` (DataFrame): One-Hot-Encoded form of the features
        """

        item_profiles = concat(
            CBRecommender.clean_and_encode(features), axis=1)
        return item_profiles

    @ensure_type([DataFrame, list], instance_method=True)
    def fit(self, train_item_profiles: DataFrame, scores: list) -> DataFrame:
        """
        Builds the user_profile by extracting user's preference from the train_item_profiles and associated scores.

        Args:
            `train_item_profiles` (DataFrame): item profiles used for building the user_profile.
                Example: item_profiles of watched movies

            `scores` (float): Score associated to each item in train_item_profiles
                Example: User rating for each watched movie

        Returns:
            `user_profile` (DataFrame): The preference model built for the user, which will be used for recommending.
        """

        if len(train_item_profiles.index) != len(scores):
            raise ValueError(
                f'train_item_profiles and scores should be equal in length, got {len(train_item_profiles.index)} and {len(scores)} instead.')

        feature_matrix = train_item_profiles.values
        score_matrix = array(scores, ndmin=2)
        profile_matrix = score_matrix.dot(feature_matrix)
        normalized_profile_matrix = profile_matrix / profile_matrix.sum()

        self.__user_profile = DataFrame(
            normalized_profile_matrix, columns=train_item_profiles.columns)
        return self.user_profile

    @ensure_type([DataFrame, DataFrame, float, int], instance_method=True)
    def recommend(self, test_items: DataFrame, test_item_profiles: DataFrame, min_score: float = 7.5, limit: int = -1) -> DataFrame:
        """
        Recommend items based on user_profile

        Args:
            `test_items` (DataFrame) Items from which recommendation is needed

            `test_item_profiles` (DataFrame): Profile of each item in test_items.
                Example: item_profiles of unwatched movies

            `min_score` (float): Minimum score used as threshold value in recommending items. Default is 7.5

            `limit` (int): Number of items to recommend

        Returns:
            `recommendations` (DataFrame): DataFrame with the test_item and predicted score.
        """

        if set(test_item_profiles.columns) != set(self.user_profile.columns):
            raise ValueError(
                f'test_item_profiles features should be same as that used in fit(). Expected {list(self.user_profile.columns)}, got {list(test_item_profiles.columns)} instead')

        items = test_items.squeeze()
        feature_matrix = test_item_profiles.values
        expected_scores = (
            feature_matrix * self.user_profile.values).sum(axis=1) * 10

        recommendations = DataFrame({
            'Item': items,
            'Expected Score': expected_scores}).sort_values('Expected Score', ascending=False)
        return recommendations[recommendations['Expected Score'] >= min_score].iloc[:limit, :]

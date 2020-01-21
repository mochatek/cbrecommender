import pandas as pd
import numpy as np

class cbr:
    def __init__(self):
        self.user_profile = None
        
    # OneHotEncode features
    def encode_features(self, features):
        if isinstance(features, pd.DataFrame):
            features = features.squeeze()
        features = features.apply(lambda g:g.lower().replace(' ', ''))
        features = features.str.get_dummies(sep = ',')
        return features

    # Extract user preferences and build User-Profile
    def fit(self, features, score):
        feature_matrix = features.values
        score_matrix = np.array(score, ndmin = 2)
        profile_matrix = score_matrix.dot(feature_matrix)
        sum = profile_matrix.sum()
        profile_matrix = profile_matrix / sum
        self.user_profile =  pd.DataFrame(profile_matrix, columns = features.columns)
        return self.user_profile

    # Recommend items based on User-Profile
    def recommend(self, items, features, score = 0, num = None):
        if isinstance(items, pd.DataFrame):
            items = items.squeeze()
        feature_matrix = features.values
        expected_scores = (feature_matrix * self.user_profile.values).sum(axis = 1) * 10
        df = pd.DataFrame({
            'item' : items,
            'expected score' : expected_scores}).sort_values('expected score', ascending = False)
        return df[df['expected score'] >= score].iloc[:num, :]

from src.cbrecommender import CBRecommender
from pandas import DataFrame

data = DataFrame(
    {'movie': ['Endgame', 'Avatar', 'Titanic', 'Infinity War', 'Jurassic World', 'Black Panther',
               'Harry Potter-II', 'The Last Jedi'],
     'genre': ['Action,Adventure,Drama', 'Action,Adventure,Fantasy', 'Drama,Romance',
               'Action,Adventure,Sci-Fi', 'Action,Adventure,Sci-Fi', 'Action,Adventure,Sci-Fi',
               'Adventure,Drama,Fantasy', 'Action,Adventure,Fantasy'],
     'language': ['Tamil', 'Tamil', 'Hindi', 'Hindi', 'English', 'Malayalam', 'Hindi', 'English']
     })

recommender = CBRecommender()
encoded_genres = recommender.encode_features(data[['genre', 'language']])

watched_movie_genres = encoded_genres.iloc[:4, :]
unwatched_movie_genres = encoded_genres.iloc[4:, :]
test_items = data[['movie']].iloc[4:, :]

user_ratings = [8.5, 7.8, 7.8, 8.5]
user_profile = recommender.fit(watched_movie_genres, user_ratings)

print(recommender.user_profile)

recommendations = recommender.recommend(
    test_items, unwatched_movie_genres.iloc[:, 1:], 5.0, 2)
print(recommendations)

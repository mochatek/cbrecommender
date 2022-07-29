# cbrecommender

[![Downloads](https://static.pepy.tech/personalized-badge/cbrecommender?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/cbrecommender)
[![Downloads](https://static.pepy.tech/personalized-badge/cbrecommender?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Month)](https://pepy.tech/project/cbrecommender)
[![Downloads](https://static.pepy.tech/personalized-badge/cbrecommender?period=week&units=international_system&left_color=grey&right_color=orange&left_text=Downloads/Week)](https://pepy.tech/project/cbrecommender)

cbrecommender is a Python library for implementing Content-Based Recommendation Engines with ease!

## Installation

Install from pypi with `pip` :

```shell
pip install cbrecommender
```

## Usage

**1. Importing and initializing :**

```python
from cbrecommender import CBRecommender

recommender = CBRecommender()
```

**2. One Hot Encoding the features :**

```python
encoded_features = recommender.encode_features(features)
```

- `features` must be _DataFrame_ that signifies the user's preferences. Example: movie genres, news topics, post tags etc.

- `encoded_features()` will return a OneHot-Encoded dataframe created from the supplied features.

**3. Extracting user preferences and creating _User-Profile_ :**

```python
user_profile = recommender.fit(train_features, scores)
```

- `fit()` is where we train our recommendation model and construct the user-profile.

- `train_features` must be a sample from encoded_features. Example: OneHot-Encoded genres of watched movies.

- `scores` must be an array denoting the user's preference (as measure) corresponding to each item of the selected sample. Example: Rating for a movie, song etc.

**4. Get recommendations based on User-Profile :**

```python
recommendations = recommender.recommend(test_items, test_features, threshold_score, limit)
```

- `test_items` must be a _pandas.DataFrame_ which denote those items that the user have not used for training. Example: Unwatched movies.

- `test_features` must be the OneHot-Encoded _pandas.DataFrame_ of the features of the test_items.

- `threshold_score` must be numerical value (1-10) that specifies the threshold score for recommending items. Default is 7.5.

- `limit` must be an integer that denotes the number of items to recommended.

## Example

```python
from cbrecommender import CBRecommender
from pandas import DataFrame
```

```python
data = DataFrame(
{'movie':['Endgame','Avatar','Titanic','Infinity War','Jurassic World','Black Panther',
          'Harry Potter-II','The Last Jedi'],
 'genre':['Action,Adventure,Drama','Action,Adventure,Fantasy','Drama,Romance',
          'Action,Adventure,Sci-Fi','Action,Adventure,Sci-Fi','Action,Adventure,Sci-Fi',
          'Adventure,Drama,Fantasy','Action,Adventure,Fantasy']
})
print(data)
```

| movie           | genre                    |
| --------------- | ------------------------ |
| Endgame         | Action,Adventure,Drama   |
| Avatar          | Action,Adventure,Fantasy |
| Titanic         | Drama,Romance            |
| Infinity War    | Action,Adventure,Sci-Fi  |
| Jurassic World  | Action,Adventure,Sci-Fi  |
| Black Panther   | Action,Adventure,Sci-Fi  |
| Harry Potter-II | Adventure,Drama,Fantasy  |
| The Last Jedi   | Action,Adventure,Fantasy |

```python
recommender = CBRecommender()

# We are considering genre alone as the feature. You can include other features as well.
onehot_encoded_genres = recommender.encode_features(data[['genre']])
print(onehot_encoded_genres)
```

| action | adventure | drama | fantasy | romance | sci-fi |
| ------ | --------- | ----- | ------- | ------- | ------ |
| 1      | 1         | 1     | 0       | 0       | 0      |
| 1      | 1         | 0     | 1       | 0       | 0      |
| 0      | 0         | 1     | 0       | 1       | 0      |
| 1      | 1         | 0     | 0       | 0       | 1      |
| 1      | 1         | 0     | 0       | 0       | 1      |
| 1      | 1         | 0     | 0       | 0       | 1      |
| 0      | 1         | 1     | 1       | 0       | 0      |
| 1      | 1         | 0     | 1       | 0       | 0      |

```python
# Consider we had watched the first 4 movies. So we use it as training data to extract preferences.
# We use the user rating for the watched movies as the preference score.
watched_movie_genres = onehot_encoded_genres.iloc[:4, :]
watched_movie_ratings = [8.5,7.8,7.8,8.5]

user_profile = recommender.fit(watched_movie_genres, watched_movie_ratings)
print(recommender.user_profile)
```

| action | adventure | drama  | fantasy | romance | sci-fi |
| ------ | --------- | ------ | ------- | ------- | ------ |
| 0.2755 | 0.2755    | 0.1811 | 0.0866  | 0.0866  | 0.0944 |

```python
# We use the remaining 4 unwatched movies as test data to get recommendations from.
unwatched_movies = data[['movie']].iloc[4:,:]
unwatched_movie_genres = onehot_encoded_genres.iloc[4:,:]

# Recommend top 3 movies with minimum expected rating of 5.0
recommendations = recommender.recommend(unwatched_movies, unwatched_movie_genres, 5.0, 3)
print(recommendations)
```

| item           | expected score |
| -------------- | -------------- |
| Jurassic World | 6.45           |
| Black Panther  | 6.45           |
| The Last Jedi  | 6.37           |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License ](https://github.com/mochatek/cbrecommender/blob/master/LICENSE.txt)

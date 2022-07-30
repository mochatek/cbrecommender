# cbrecommender

[![Downloads](https://static.pepy.tech/personalized-badge/cbrecommender?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/cbrecommender)
[![Downloads](https://static.pepy.tech/personalized-badge/cbrecommender?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Month)](https://pepy.tech/project/cbrecommender)
[![Downloads](https://static.pepy.tech/personalized-badge/cbrecommender?period=week&units=international_system&left_color=grey&right_color=orange&left_text=Downloads/Week)](https://pepy.tech/project/cbrecommender)

cbrecommender is a Python library for implementing Content-Based Recommendation Engines with ease!

**A Content-Based Recommender** is a form of **Personalized recommendation System** that maintains a user profile and tries to match the items with the taste profile of a user before presenting them as a recommendation to the user.

`The key ideas are:`

> - Model items according to relevant attributes derived from the content.

> - Develop a user profile either from their implicit actions (clicks, time spend on a video etc.), explicit actions(purchase, rating etc.) or by combining both.

> - Use these profiles to provide recommendations.

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

**2. Creating _Item Profiles_ :**

In Content-Based Recommender, we must build a profile for each item, which will represent the important characteristics of that item.

```python
item_profiles = recommender.create_item_profile(features)
```

- `features: DataFrame` must be relevant attributes of the item that signifies the user's preferences. For example: movie genres, news topics, post tags etc.

- `create_item_profile() -> DataFrame` will return the item_profiles created from the supplied features.

**3. Creating _User Profile_ :**

```python
user_profile = recommender.fit(train_item_profiles, scores)
```

- `fit() -> DataFrame` is where we extract user preferences from the item-profiles and associated scores, and then construct the user-profile.

- `train_item_profiles: DataFrame` must be a subset of the item-profiles created at _step 2_. For example, it can be the item-profiles of the movies already watched by the user (watch history).

- `scores: List[float]` must be a list of some measure corresponding to each item in _train_item_profiles_, denoting how much the user liked that item. For example: Rating for a watched movie, song etc.

**4. Get recommendations based on _User Profile_ :**

```python
recommendations = recommender.recommend(test_items, test_item_profiles, min_score, limit)
```

- `test_items: DataFrame` must be those items that the user have not used for training and from which we need recommendations. For example: Unwatched movies.

- `test_item_profiles: DataFrame` must be the item-profiles of _test_items_.

- `min_score: float` must be a numerical value (1-10) that specifies the minimum score for recommending items. Default is 7.5.

- `limit: int` must be an integer that denotes the number of items to recommended.

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
movie_profiles = recommender.create_item_profile(data[['genre']])
print(movie_profiles)
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
watched_movie_profiles = movie_profiles.iloc[:4, :]
watched_movie_ratings = [8.5,7.8,7.8,8.5]

user_profile = recommender.fit(watched_movie_profiles, watched_movie_ratings)
print(recommender.user_profile)
```

| action | adventure | drama  | fantasy | romance | sci-fi |
| ------ | --------- | ------ | ------- | ------- | ------ |
| 0.2755 | 0.2755    | 0.1811 | 0.0866  | 0.0866  | 0.0944 |

```python
# We use the remaining 4 unwatched movies as test data to get recommendations from.
unwatched_movies = data[['movie']].iloc[4:,:]
unwatched_movie_profiles = movie_profiles.iloc[4:,:]

# Recommend top 3 movies with minimum expected rating of 5.0
recommendations = recommender.recommend(unwatched_movies, unwatched_movie_profiles, 5.0, 3)
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

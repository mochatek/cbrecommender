# cbrecommender

cbrecommender is a Python library for implementing a Content-Based Recommendation Engine.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cbrecommender.

```bash
pip install cbrecommender
```

## Usage

```python
# Import the class 'cbr' for Content-Based Recommender.
from cbrecommender import cbr

# Create the object.
r = cbr()

# OneHotEncode the features
r.encode_features(features)
''' 
* features(pandas.DataFrame) can be anything that signifies the user's preferences.
* For example, movie genres, news topics, post tags etc.
* Returns a OneHotEncoded dataframe from the features's comma (,) separated values.
'''

# Extract user's preferences and build the 'User-Profile'.
r.fit(features, scores)
''' 
* features(pandas.DataFrame) must be OneHotEncoded and is that of the items of user's choice.
* scores(list) denote the user's preference to the corresponding items.
* For example, it can be rating for a movie, song etc. 
* Returns the 'User-Profile', which is the model.
 '''
# Recommend items based on User-Profile.
r.recommend(items, features, [score, num])
''' 
* items(pandas.DataFrame) which denote those items that the user haven't chosen.
* features(pandas.DataFrame) is that of the items.
* score(float) is a non-mandatory parameter that specifies the threshold score for recommending items.
* num(int) is also a non-mandatory parameter that denotes the number of items to be recommended.
* Returns items along with their expected_score as a pandas.DataFrame object.
'''
```

## Example
```python
from cbrecommender import cbr
import pandas
```
```python
df = pandas.DataFrame(
{'movie':['Endgame','Avatar','Titanic','Infinity War','Jurassic World','Black Panther',
          'Harry Potter-II','The Last Jedi'],
 'genre':['Action,Adventure,Drama','Action,Adventure,Fantasy','Drama,Romance',
          'Action,Adventure,Sci-Fi','Action,Adventure,Sci-Fi','Action,Adventure,Sci-Fi',
          'Adventure,Drama,Fantasy','Action,Adventure,Fantasy']
})
print(df)
```
| movie | genre |
--------|--------
|Endgame|Action,Adventure,Drama|
|Avatar|Action,Adventure,Fantasy|
|Titanic|Drama,Romance|
|Infinity War|Action,Adventure,Sci-Fi|
|Jurassic World|Action,Adventure,Sci-Fi|
|Black Panther|Action,Adventure,Sci-Fi|
|Harry Potter-II|Adventure,Drama,Fantasy|
|The Last Jedi|Action,Adventure,Fantasy|

```python
r = cbr()
gen = r.encode_features(df.genre)
print(gen)
```
| action | adventure | drama | fantasy | romance | sci-fi |
-------|-------|--------|---------|------|------|
|1|1|1|0|0|0|
|1|1|0|1|0|0|
|0|0|1|0|1|0|
|1|1|0|0|0|1|
|1|1|0|0|0|1|
|1|1|0|0|0|1|
|0|1|1|1|0|0|
|1|1|0|1|0|0|

```python
rating = [8.5,7.8,7.8,8.5]
model = r.fit(gen.iloc[:4, :], rating)
print(c.user_profile)
```
| action | adventure | drama | fantasy | romance | sci-fi |
-------|-------|--------|---------|------|------|
|0.2755|0.2755|0.1811|0.0866|0.0866|0.0944|

```python
recommendations = r.recommend(df[['movie']].iloc[4:,:], gen.iloc[4:,:])
print(recommendations)
```
| item| expected score |
--------|--------
|Jurassic World|6.45|
|Black Panther|6.45|
|Harry Potter-II|6.37|
|The Last Jedi|5.43|

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT License ](https://github.com/mochatek/cbrecommender/blob/master/LICENSE.txt)
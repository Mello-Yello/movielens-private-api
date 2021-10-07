# movielens-private-api
Unofficial Python API for the Movielens unpublished API, using the `requests` module. Tested with Python 2.7 and 3.6, but should be compatible with more.

### Installing movielens-private-api
You can either clone the repository and install the package with pip:
```shell
$ git clone git://github.com/Mello-Yello/movielens-private-api.git
$ cd movielens-private-api
$ python -m pip install .
```

Or directly from PyPI:
```shell
$ python -m pip install movielens-private-api
```

## Usage

### Setup

Since operations are performed on a specific account, you need to either log in or provide the HTTP cookie containing a valid session.



```python
from movielens_private_api import Movielens
m = Movielens()
cookie = m.login(username, password)
```

The variable *cookie* from above can be saved to a file to be reused later during class initialization

```python
from movielens_private_api import Movielens
m = Movielens(cookie)
```

### Exceptions

If the class wasn't initiated with a cookie, calling any method before `login()` will raise a `MovielensException`. This class encapsulates any API error received in the response, and is raised after an improper request. To access the original error message you have to catch the exception and use `str()` on it. 

```python
from movielens_private_api import Movielens, MovielensException
m = Movielens()

try:
    m.getMe()
except MovielensException as e:
    msg = str(e)
    print(msg)
--------------------------------------
Output: "authenticated user required"
```

### Movielens

```python
Movielens(cookie=None, timeoutSececonds=30, api_endpoint='https://movielens.org/api/', verifySSL=True)
```

- `cookie`: The HTTP cookie for movielens with a valid session 
- `timeoutSececonds`: An exception is raised if the server has not issued a response for *timeoutSececonds* seconds
- `api_endpoint`: The api endpoint to connect to
- `verifySSL`: Whether or not to verify SSL


## User info methods

### login(email, password)
Logs into the provided account, and returns the HTTP cookie

### getMe()
Obtain information about the user: number of movies rated, email, username, time of account creation, time of last login, preferences, recommender used, ...

### getMyTags()
Statistics on movie related tags the user has left on different films. E.g. desert, black comedy, zombie

### getMyStats()
History of ratings, rating distribution, list of movies rated much more or much less that the average.


## Movie exploration / search

All of the methods here have the *params* parameter, a dictionary with parameters to pass to the request. Possible parameters are listed in the documentation for *explore()*. *params* is optional for all the methods, and if provided is forwarded to *explore()*

### explore(params)
Used to query Movielens, it can perform searches with various parameters.

* `q`: *string* --> Is used to specify the title search
* `sortBy`: *string* --> Possible values include: *prediction*, *releaseDate*, *avgRating*, *dateAdded*, *userRatedDate*, *userListedDate*
* `hasWishlisted`: *string* in ['yes', 'no', 'ignore'] --> Show wishlisted movies only
* `hasRated`: *string* in ['yes', 'no'', 'ignore'] --> Show rated movies only
* `hasHidden`: *string* in ['yes', 'no'', 'ignore'] --> Show hidden movies only



```
m.explore({'q': 'Dune'})
```

### topPicks(params)
Returns suggested movies based on the given ratings and the chosen recommender

### recentReleases(params)
Returns recently released movies


### favoritesYear(params)
Returns a selection of higly rated movies from the previous year

### newAdditions(params)
Returns movies recently added to Movielens

### getMyRatings(params)
Returns movies rated by the user

### getMyWishlist(params)
Returns movies added to the whishlist by the user

### getMyHiddenMovies(params)
Returns movies hidden by the user


## Movie operations

### rate(movieId, rating)
Rate a movie on a scale from 0 to 5, with half values (like 3.5) accepted.

### addToWishlist(movieId)
Add a movie to the user whishlist

### hide(movieId)
Hide a movie from the user. Equivalent to rating the movie -1

### removeFromWishlist(movieId)
Remove a movie from the user whishlist

### resetRating(movieId)
Delete the rating for the given movie.

### unhide(movieId)
Unhide a hidden movie. Calls resetRating()


### getMovieInfo(movieId)
Returns both the movie info and the interaction the user had with the movie (rating, hidden, wishlisted, predicted score, ....)


## Miscellaneous

### getGenres()
Statistics on how many movies are in Movielens, divided by genre. Also the most frequent tags for each genre
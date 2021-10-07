import json
import requests

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

class MovielensException(Exception):
        def __init___(self, errorMessage):
            self.message = "Movielens error: {0}".format(errorMessage)
            super().__init__(self.message)

class Movielens:
    def __init__(self,  cookie = None,
                        timeoutSececonds = 30,
                        api_endpoint = 'https://movielens.org/api/',
                        verifySSL = True):
        
        """
        Parameters
        ----------
        cookie : str, optional
            The HTTP cookie for movielens with a valid session
        timeoutSececonds : float, optional
            An exception is raised if the server has not issued a response after timeoutSececonds
        api_endpoint : str, optional
            The api endpoint to connect to
        verifySSL : bool, optional
            Whether or not to verify SSL
        """
        
        self.verifySSL = verifySSL
        self.baseURL = api_endpoint
        self.timeout = timeoutSececonds
        
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'DNT': '1',
            'Host': 'movielens.org',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
        }
        
        if cookie:
            self.headers['cookie'] = cookie
    
    def login(self, username, password):
        '''Logs into the provided account, and returns the HTTP cookie'''
        headers = { 'Referer': 'https://movielens.org/login' }
        response = self.__post('sessions', { 'userName': username, 'password': password }, headers, retRequestsResponse = True)
        cookie = response.headers['set-cookie']
        self.headers['cookie'] = cookie
        return cookie
    
    def __checkException(self, response):
        r = json.loads(response.text)
        if r["status"] == "error":
            raise MovielensException(r["message"])
        
        assert r["status"] == "success"
     
    def __cleanResponse(self, response, retRequestsResponse):
        self.__checkException(response)
        
        if retRequestsResponse:
            return response
        else:
            j =  json.loads(response.text)
            if 'data' in j.keys():
                return j['data']
            else:
                return None
     
    def __post(self, resource, params = None, headers = None, retRequestsResponse = False):
        if params is None: params = {}
        if headers is None: headers = {}
        r = requests.post(
            self.baseURL+resource, 
            json = params, 
            headers = merge_dicts(self.headers, headers), 
            verify=self.verifySSL,
            timeout=self.timeout)
        return self.__cleanResponse(r, retRequestsResponse)
    
    def __get(self, resource, params = None, headers = None, retRequestsResponse = False):
        if params is None: params = {}
        if headers is None: headers = {}
        r = requests.get(
            self.baseURL+resource, 
            params = params,
            headers = merge_dicts(self.headers, headers), 
            verify=self.verifySSL,
            timeout=self.timeout)
        return self.__cleanResponse(r, retRequestsResponse)
    
    def __delete(self, resource, params = None, headers = None, retRequestsResponse = False):
        if params is None: params = {}
        if headers is None: headers = {}
        r = requests.delete(
            self.baseURL+resource, 
            params = params,
            headers = merge_dicts(self.headers, headers), 
            verify=self.verifySSL,
            timeout=self.timeout)
        return self.__cleanResponse(r, retRequestsResponse)
    
    def getMe(self):
        '''Obtain information about the user: number of movies rated, email, username, time of account creation, time of last login, preferences, recommender used, ...'''
        return self.__get('users/me')
    
    def getGenres(self):
        '''Statistics on how many movies are in Movielens, divided by genre. Also the most frequent tags for each genre'''
        return self.__get('movies/genres')
    
    def getMyTags(self):
        '''Statistics on movie related tags the user has left on different films. E.g. desert, black comedy, zombie'''
        return self.__get('users/me/tags')
    
    def explore(self, params = None):
        '''Used to query Movielens, it can perform searches with various parameters.'''
        
        """
        Parameters
        ----------
        params: dict, optional
            a dictionary parameter:value to be passed as arguments to the request
            
            {
                q : str, optional
                    Used to specify the title search
                sortBy : string, optional
                    Possible values include: 'prediction', 'releaseDate', 'avgRating', 'dateAdded', 'userRatedDate', 'userListedDate'
                hasWishlisted : str, optional
                    Show wishlisted movies only: ['yes', 'no', 'ignore']
                hasRated : str, optional
                    Show rated movies only: ['yes', 'no', 'ignore']
                hasHidden : str, optional
                    Show hidden movies only: ['yes', 'no', 'ignore']
            }
        """
        
        if params is None: params = {}
        return self.__get('movies/explore', params)
    
    def topPicks(self, params = None):
        '''Returns suggested movies based on the given ratings and the chosen recommender'''
        if params is None: params = {}
        newParams = {
            'hasRated': 'no',
            'sortBy': 'prediction',
        }
        return self.explore(merge_dicts(newParams, params))
    
    def recentReleases(self, params = None):
        '''Returns recently released movies'''
        if params is None: params = {}
        newParams = {
            'sortBy': 'releaseDate',
            'hasRated': 'no',
            'maxDaysAgo': 90,
            'maxFutureDays': 0,
        }
        return self.explore(merge_dicts(newParams, params))
    
    def favoritesYear(self, params = None):
        '''Returns a selection of higly rated movies from the previous year'''
        if params is None: params = {}
        newParams = {
            'sortBy': 'avgRating',
            'hasRated': 'no',
            'maxDaysAgo': 365,
            'maxFutureDays': 0,
            'minPop': 100,
        }
        return self.explore(merge_dicts(newParams, params))
    
    def newAdditions(self, params = None):
        '''Returns movies recently added to Movielens'''
        if params is None: params = {}
        newParams = {
            'sortBy': 'dateAdded',
        }
        return self.explore(merge_dicts(newParams, params))
    
    def getMyRatings(self, params = None):
        '''Returns movies rated by the user'''
        if params is None: params = {}
        newParams = {
            'sortBy': 'userRatedDate',
            'hasRated': 'yes',
        }
        return self.explore(merge_dicts(newParams, params))
    
    def getMyWishlist(self, params = None):
        '''Returns movies added to the whishlist by the user'''
        if params is None: params = {}
        newParams = {
            'sortBy': 'userListedDate',
            'hasWishlisted': 'yes',
        }
        return self.explore(merge_dicts(newParams, params))
    
    def getMyHiddenMovies(self, params = None):
        '''Returns movies hidden by the user'''
        if params is None: params = {}
        newParams = {
            'hasHidden': 'yes',
        }
        return self.explore(merge_dicts(newParams, params))
    
    def getMyStats(self):
        '''History of ratings, rating distribution, list of movies rated much more or much less that the average.'''
        return self.__get('users/me/ratings/stats')
    
    def rate(self, movieId, rating):
        '''Rate a movie on a scale from 0 to 5, with half values (like 3.5) accepted.'''
        return self.__post('users/me/ratings', { "movieId": movieId, "predictedRating": 5, "rating": rating })
    
    def addToWishlist(self, movieId):
        '''Add a movie to the user whishlist'''
        return self.__post('users/me/wishlist', { "movieId": movieId })
    
    def hide(self, movieId):
        '''Hide a movie from the user. Equivalent to rating the movie -1'''
        return self.rate(movieId, -1)
    
    def removeFromWishlist(self, movieId):
        '''Remove a movie from the user whishlist'''
        return self.__delete('users/me/wishlist/{0}'.format(movieId))
    
    def unhide(self, movieId):
        '''Unhide a hidden movie. Calls resetRating()'''
        return self.resetRating(movieId)
    
    def resetRating(self, movieId):
        '''Delete the rating for the given movie.'''
        return self.__delete('users/me/ratings/{0}'.format(movieId))
    
    def getMovieInfo(self, movieId):
        '''Returns both the movie info and the interaction the user had with the movie (rating, hidden, wishlisted, predicted score, ....)'''
        return self.__get('movies/{0}'.format(movieId))
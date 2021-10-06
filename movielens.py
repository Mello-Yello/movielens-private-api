import json
import requests

class MovielensException(Exception):
        def __init___(self, errorMessage):
            self.message = "Movielens error: {0}".format(errorMessage)
            super().__init__(self.message)

class Movielens:
    def __init__(self,  cookie = None,
                        timeoutSececonds = 30,
                        api_endpoint = 'https://movielens.org/api/',
                        verifySSL = True):
        
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
    
    def login(self, username: str, password: str) -> str:
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
            headers = {**self.headers, **headers}, 
            verify=self.verifySSL,
            timeout=self.timeout)
        return self.__cleanResponse(r, retRequestsResponse)
    
    def __get(self, resource, params = None, headers = None, retRequestsResponse = False):
        if params is None: params = {}
        if headers is None: headers = {}
        r = requests.get(
            self.baseURL+resource, 
            params = params, 
            headers = {**self.headers, **headers}, 
            verify=self.verifySSL,
            timeout=self.timeout)
        return self.__cleanResponse(r, retRequestsResponse)
    
    def __delete(self, resource, params = None, headers = None, retRequestsResponse = False):
        if params is None: params = {}
        if headers is None: headers = {}
        r = requests.delete(
            self.baseURL+resource, 
            params = params, 
            headers = {**self.headers, **headers}, 
            verify=self.verifySSL,
            timeout=self.timeout)
        return self.__cleanResponse(r, retRequestsResponse)
    
    def getMe(self):
        return self.__get('users/me')
    
    def getGenres(self):
        return self.__get('movies/genres')
    
    def getMyTags(self):
        return self.__get('users/me/tags')
    
    def explore(self, params = None):
        if params is None: params = {}
        return self.__get('movies/explore', params)
    
    def topPicks(self, params = None):
        if params is None: params = {}
        newParams = {
            'hasRated': 'no',
            'sortBy': 'prediction',
        }
        return self.explore({**newParams, **params})
    
    def recentReleases(self, params = None):
        if params is None: params = {}
        newParams = {
            'sortBy': 'releaseDate',
            'hasRated': 'no',
            'maxDaysAgo': 90,
            'maxFutureDays': 0,
        }
        return self.explore({**newParams, **params})
    
    def favoritesYear(self, params = None):
        if params is None: params = {}
        newParams = {
            'sortBy': 'avgRating',
            'hasRated': 'no',
            'maxDaysAgo': 365,
            'maxFutureDays': 0,
            'minPop': 100,
        }
        return self.explore({**newParams, **params})
    
    def newAdditions(self, params = None):
        if params is None: params = {}
        newParams = {
            'sortBy': 'dateAdded',
        }
        return self.explore({**newParams, **params})
    
    def getMyRatings(self, params = None):
        if params is None: params = {}
        newParams = {
            'sortBy': 'userRatedDate',
            'hasRated': 'yes',
        }
        return self.explore({**newParams, **params})
    
    
    def getMyWishlist(self, params = None):
        if params is None: params = {}
        newParams = {
            'sortBy': 'userListedDate',
            'hasWishlisted': 'yes',
        }
        return self.explore({**newParams, **params})
    
    def getMyHiddenMovies(self, params = None):
        if params is None: params = {}
        newParams = {
            'hasHidden': 'yes',
        }
        return self.explore({**newParams, **params})
    
    def getMyStats(self):
        return self.__get('users/me/ratings/stats')
    
    def rate(self, movieId, rating):
        return self.__post('users/me/ratings', { "movieId": movieId, "predictedRating": 5, "rating": rating })
    
    def addToWishlist(self, movieId):
        return self.__post('users/me/wishlist', { "movieId": movieId })
    
    def hide(self, movieId):
        return self.rate(movieId, -1)

    def removeFromWishlist(self, movieId):
        return self.__delete('users/me/wishlist/{0}'.format(movieId))

    def unhide(self, movieId):
        return self.resetRating(movieId)
    
    def resetRating(self, movieId):
        return self.__delete('users/me/ratings/{0}'.format(movieId))
    
    def getMovieInfo(self, movieId):
        return self.__get('movies/{0}'.format(movieId))
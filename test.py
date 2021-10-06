import unittest
from movielens import Movielens

MOVIE_ID = 2021 # Dune (1984)

def iterMovies(response):
    for movie in response['searchResults']:
        yield movie

class TestSearch(unittest.TestCase):
    def test_movie_search(self):
        duneId = 254726
        movieIds = [movie['movieId'] for movie in iterMovies(m.explore({'q': 'Dune'}))]    
        self.assertIn(duneId, movieIds)

class TestCredentials(unittest.TestCase):
    def test_a_login(self):
        cookie = m.login(username, password)
        self.assertIn('Expires', cookie)
    
    def test_email_check(self):
        accountEmail = m.getMe()['account']['email']
        self.assertEqual(username, accountEmail)


class TestMovieInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        movieData = m.getMovieInfo(MOVIE_ID)['movieDetails']['movieUserData']
        cls._rating = movieData['rating']
        cls._wishlist = movieData['wishlist']
        cls._hidden = movieData['hidden']
        
        if cls._hidden: m.unhide(MOVIE_ID)
        if cls._wishlist: m.removeFromWishlist(MOVIE_ID)
        m.resetRating(MOVIE_ID)
    
    @classmethod
    def tearDownClass(cls):
        if cls._hidden: m.hide(MOVIE_ID)
        if cls._wishlist: m.addToWishlist(MOVIE_ID)
        if cls._rating: m.rate(MOVIE_ID, cls._rating)
    
    def testHiddenlist(self):
        movieIdsHidden = [movie['movieId'] for movie in iterMovies(m.getMyHiddenMovies())]
        self.assertNotIn(MOVIE_ID, movieIdsHidden)
        m.hide(MOVIE_ID)
        movieIdsHidden = [movie['movieId'] for movie in iterMovies(m.getMyHiddenMovies())]
        self.assertIn(MOVIE_ID, movieIdsHidden)
        
        m.unhide(MOVIE_ID)
        movieIdsHidden = [movie['movieId'] for movie in iterMovies(m.getMyHiddenMovies())]
        self.assertNotIn(MOVIE_ID, movieIdsHidden)
        
    def testRating(self):
        movieIdsRated = [movie['movieId'] for movie in iterMovies(m.getMyRatings())]
        self.assertNotIn(MOVIE_ID, movieIdsRated)
        m.rate(MOVIE_ID, 5)
        movieIdsRated = [movie['movieId'] for movie in iterMovies(m.getMyRatings())]
        self.assertIn(MOVIE_ID, movieIdsRated)

    def testStats(self):
        movieIdsRated = [movie['movieId'] for movie in iterMovies(m.getMyRatings())]
        if not MOVIE_ID in movieIdsRated:
            startingNumberRated = m.getMyStats()['numberRated']
            m.rate(MOVIE_ID, 5)
            endingNumberRated = m.getMyStats()['numberRated']
        else:
            endingNumberRated = m.getMyStats()['numberRated']
            m.resetRating(MOVIE_ID)
            startingNumberRated = m.getMyStats()['numberRated']
        
        self.assertEqual(startingNumberRated + 1, endingNumberRated)

    def testWishlist(self):
        movieIdsWishlist = [movie['movieId'] for movie in iterMovies(m.getMyWishlist())]
        self.assertNotIn(MOVIE_ID, movieIdsWishlist)
        m.addToWishlist(MOVIE_ID)
        movieIdsWishlist = [movie['movieId'] for movie in iterMovies(m.getMyWishlist())]
        self.assertIn(MOVIE_ID, movieIdsWishlist)
        
        m.removeFromWishlist(MOVIE_ID)
        movieIdsWishlist = [movie['movieId'] for movie in iterMovies(m.getMyWishlist())]
        self.assertNotIn(MOVIE_ID, movieIdsWishlist)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestCredentials))
    suite.addTests(unittest.makeSuite(TestSearch))
    suite.addTests(unittest.makeSuite(TestMovieInteraction))
    return suite

if __name__ == '__main__':
    username = input("Insert username for Movielens: ")
    password = input("Insert password for Movielens: ")
    
    m = Movielens()
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
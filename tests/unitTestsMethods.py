import unittest
from unittest.mock import MagicMock, AsyncMock
from Reverse_Twitter_Scraper import TwitterScraper

class TestTwitterScraper(unittest.TestCase):

    def setUp(self):
        self.twitter_handles = ["elonmusk", "POTUS", "BitcoinMagazine"]
        self.chromedriver_path = "C:/Program Files (x86)/chromedriver.exe"
        self.cookies = ""
        self.proxy_list = ""

        self.scraper = TwitterScraper(self.twitter_handles, self.chromedriver_path, self.cookies, self.proxy_list)
        
        self.singlePlainTweet = self.scraper.getTweetsPlain()[0]['resp'][0]
        self.singleUserPlain = self.scraper.getUserPlain()[0]

    # def test_getUserPlain(self):
    #     result = self.scraper.getUserPlain()
    #     self.assertIsInstance(result, list)
    #     self.assertGreater(len(result), 0)
    #     for user in result:
    #         self.assertIn('handle', user)
    #         self.assertIsInstance(user['id'], str)
    #         self.assertIsInstance(user['resp'], dict)

    # def test_getTweetsPlain(self):
    #     result = self.scraper.getTweetsPlain()
    #     self.assertIsInstance(result, list)
    #     self.assertGreater(len(result), 0)
    #     for user in result:
    #         self.assertIn('handle', user)
    #         self.assertIsInstance(user['id'], str)
    #         self.assertIsInstance(user['resp'], list)

    # def test_getTweetsText(self):
    #     result = self.scraper.getTweetsText()
    #     self.assertIsInstance(result, list)
    #     self.assertGreater(len(result), 0)
    #     for user in result:
    #         self.assertIn('handle', user)
    #         self.assertIsInstance(user['id'], str)
    #         self.assertIsInstance(user['tweets'], list)
    #         for tweet in user['tweets']:
    #             self.assertIsInstance(tweet['entryId'], str)
    #             self.assertIsInstance(tweet['retweet'], bool)
    #             self.assertIsInstance(tweet['text'], str)


if __name__ == '__main__':
    unittest.main()

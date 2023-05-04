import unittest
from unittest.mock import MagicMock, AsyncMock
from ReverseTwitterScraper import TwitterScraper

class TestTwitterScraper(unittest.TestCase):
    
    def setUp(self):
        self.twitter_handles = ["elonmusk", "POTUS", "BitcoinMagazine"]
        self.chromedriver_path = "C:/Program Files (x86)/chromedriver.exe"
        self.cookies = ""
        self.proxy_list = ""

    # def test_init(self):
    #     self.twitter_handles = ["elonmusk", "POTUS", "BitcoinMagazine"]
    #     self.chromedriver_path = "C:/Program Files (x86)/chromedriver.exe"
    #     cookies = ""
    #     proxies = ""
    #     scraper = TwitterScraper(self.twitter_handles, self.chromedriver_path, cookies, proxies)
        
    #     self.assertEqual(scraper._TwitterScraper__twitterHandle, self.twitter_handles)
    #     self.assertEqual(scraper._TwitterScraper__chromedriverPath, self.chromedriver_path)
    #     self.assertEqual(scraper._TwitterScraper__accCookies, cookies)
    #     self.assertIsNone(scraper.proxies)

    # def test_cookieDict_str(self):        
    #     cookies = "cookie1=value1; cookie2=value2"
    #     expected_dict = {"cookie1": "value1", "cookie2": "value2"}
    #     scraper = TwitterScraper(self.twitter_handles, self.chromedriver_path, cookies)
        
    #     self.assertEqual(scraper.cookieDict(cookies), expected_dict)

    # def test_cookieDict_dict(self):
    #     cookies = {"cookie1": "value1", "cookie2": "value2"}
    #     scraper = TwitterScraper(self.twitter_handles, self.chromedriver_path, cookies)
    #     self.assertEqual(scraper.cookieDict(cookies), cookies)

    # def test_changeProxy_no_proxies(self):
    #     scraper = TwitterScraper(self.twitter_handles, self.chromedriver_path, proxyList=None)
    #     self.assertIsNone(scraper.changeProxy())

    # async def test_getID(self):
    #     handle = "elonmusk"
    #     scraper = TwitterScraper(handle, self.chromedriver_path)
    #     mock_client = AsyncMock()
    #     mock_client.post.return_value.text = "44196397"
    #     result = await scraper._TwitterScraper__getID(mock_client, handle)
    #     self.assertEqual(result, {"handle": handle, "id": "44196397"})

    # async def test_getTwitterIDs(self):
    #     mock_scraper = MagicMock(spec=TwitterScraper)
    #     mock_scraper._TwitterScraper__twitterHandle = self.twitter_handles
    #     ids = await mock_scraper._TwitterScraper__getTwitterIDs()
    #     self.assertEqual(ids, [{"handle": "elonmusk", "id": "44196397"},
    #                            {"handle": "POTUS", "id": "1349149096909668363"},
    #                            {"handle": "BitcoinMagazine", "id": "361289499"}])

if __name__ == "__main__":
    unittest.main()

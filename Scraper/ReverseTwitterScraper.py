import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import requests

class ReverseTwitterScraper:

    def cookieDict(self, cookies):
        if type(cookies) == dict:
            pass
        elif type(cookies) == str:
            _cookies = cookies.split("; ")
            cookies = {}
            for cookie in _cookies:
                _cookie = cookie.split("=")
                try:
                    cookies[_cookie[0]] = _cookie[1]
                except Exception as e:
                    print(e)
        else:
            exit(
                f"Twitter | Type: {type(cookies)} is currently unsupported for cookies, if you'd like to see it added please open an issue on Github")

        return cookies

    def __init__(self, twitterHandle, chromedriverPath, cookies="", timeout=3, proxies=""):
        """
        makes everything ready to scrape twitter.

        :param str twitterHandle: e.g. https://twitter.com/elonmusk -> handle = elonmusk
        :param str chromedriverPath: e.g. C:/Program Files (x86)/chromedriver.exe
        :param int sleep: default=3, if the page doesn't load in time, upper this value
        """

        #format proxy
        if proxies != "" and proxies != None:
            __split = str(proxies).split(":")
            self.proxies = {'https': f'http://{__split[2]}:{__split[3]}@{__split[0]}:{__split[1]}'}
        else:
            self.proxies = None

        wireOptions = {
            'proxy': self.proxies
        }

        print("gathering meta-information")
        # get driver
        options = Options()
        options.add_argument("--headless")
        #driver = webdriver.Chrome(chromedriverPath, options=options)
        driver = webdriver.Chrome(chromedriverPath, seleniumwire_options=wireOptions, options=options)



        #get main URL
        driver.get(f"https://twitter.com/{twitterHandle}")
        time.sleep(timeout)  # sleep to let the twitter page load

        self.__headersDict = {}
        for headerReq in driver.requests:
            url = headerReq.url
            if "UserTweets" in url and "cursor" not in url:
                self.__reqUrl = url
                self.__userID = url.split("userId%22%3A%22")[1].split("%22%2C%22count%22")[0]
                self.__headersDict = dict(headerReq.headers)
        time.sleep(1)
        driver.close()

        self.__headers = {
            'authorization': self.__headersDict['authorization'],
            'cookie': self.__headersDict['cookie'],
            'user-agent': self.__headersDict['user-agent'],
            'x-csrf-token': self.__headersDict['x-csrf-token'],
            'x-guest-token': self.__headersDict['x-guest-token']
        }
        print("Done!")

        #check for cookies and proxies
        if cookies != "":
            #get dummy URL to set cookies
            driver.get("https://twitter.com")
            self.__cookies = self.cookieDict(cookies)
            for key, value in self.__cookies.items():
                driver.add_cookie({'name': key, 'value': value, "domain": ".twitter.com"})
        else:
            self.__cookies = self.cookieDict(self.__headersDict['cookie'])

        self.__session = requests.session()
        self.__openingResp = self.__session.get(url=self.__reqUrl, headers=self.__headers, cookies=self.__cookies, proxies=self.proxies)
        self.__openingResp = self.__openingResp.json()  #may throw a JsonDecodeError when you get ratelimited
        self.__userResp = self.__openingResp['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][0]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']


    def closeSession(self):
        self.__session.close()
        self.__headers = None
        self.__openingResp = None
        self.__userResp = None
        self.__reqUrl = None
        self.__cookies = None
        self.proxies = None

    def getAllAccData(self):
        """
        returns all (unfiltered) data for the account
        """
        return self.__openingResp.json()

    #get Tweet data
    def getRetweetInfo(self, singlePlainTweet, getRetweetInfo=False):
        """
        checks if the tweet is a retweet (returns True/False/TweetInfo)

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getAllTweetsPlain to get the info
        :param getRetweetInfo: default=False -> get all info about the retweetet tweet
        """

        if 'retweeted_status_result' in singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']:
            if getRetweetInfo:
                return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['retweeted_status_result']
            else:
                return True
        else:
            return False

    def getAllTweetsPlain(self):
        """
        get all (unfiltered) tweets from an account
        """

        resp = self.__session.get(url=self.__reqUrl, headers=self.__headers, cookies=self.__cookies, proxies=self.proxies)
        return resp.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']

    def getAllTweetsText(self):
        """
        get text from all tweets from an account
        """
        resp = self.__session.get(url=self.__reqUrl, headers=self.__headers, cookies=self.__cookies, proxies=self.proxies).json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']
        tweets = []
        for tweet in resp:
            try:
                tweets.append({
                    'entryId': tweet['entryId'],
                    'retweet': self.getRetweetInfo(tweet),
                    'text': tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text']})
            except:
                continue
        return tweets

    def getCreatedAt(self, singlePlainTweet):
        """
        returns createTimeDate of a tweet

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getAllTweetsPlain to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['created_at']

    def getID(self, singlePlainTweet):
        """
        returns the ID of a tweet

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getAllTweetsPlain to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['id_str']

    def getRetweetCount(self, singlePlainTweet):
        """
        returns how many times the tweet has been retweeted

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getAllTweetsPlain to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count']

    def getReplyCount(self, singlePlainTweet):
        """
        returns how many replies the tweet has

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getAllTweetsPlain to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['reply_count']

    def getViews(self, singlePlainTweet):
        """
        returns how many views the tweet has

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getAllTweetsPlain to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['views']['count']

    def getPinnedTweetInfo(self):
        """
        returns all (unfiltered) information about the pinned tweet
        """
        return self.__openingResp['data']['user']['result']['timeline_v2']['timeline']['instructions'][2]['entry']['content']['itemContent']['tweet_results']['result']


    #get User data
    def isBusinessAccount(self):
        """
        returns if the account is a business account
        """
        return self.__userResp['business_account']

    def hasNftAvatar(self):
        """
        returns if the account has an NFT avatar
        """
        return self.__userResp['has_nft_avatar']

    def userID(self):
        """
        returns if the account has an NFT avatar
        """
        return self.__userResp['id']

    def isBlueVerified(self):
        """
        returns if the account is verified with a twitter blue check
        """
        return self.__userResp['is_blue_verified']

    def createdAt(self):
        """
        returns the creation time of an account
        """
        return self.__userResp['legacy']['created_at']

    def description(self):
        """
        returns the description of an account
        """
        return self.__userResp['legacy']['description']

    def getAllUserData(self):
        """
        returns all (unfiltered) data about an account
        """
        return self.__userResp

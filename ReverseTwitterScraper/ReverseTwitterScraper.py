import time
import traceback

import asyncio
import aiohttp
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import requests


class simpleTwitterScraper:

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

    def changeProxy(self):
        if self.proxies:
            return self.proxies[self.__proxyCounter]
        else:
            return None


    def __init__(self, twitterHandle, chromedriverPath, cookies="", timeout=5, proxyList=""):
        """
        makes everything ready to scrape twitter.

        :param str twitterHandle: e.g. https://twitter.com/elonmusk -> handle = elonmusk or array with multiple handles ["elonmusk", "POTUS", "BitcoinMagazine"]
        :param str chromedriverPath: e.g. C:/Program Files (x86)/chromedriver.exe
        :param str cookies: your twitter account cookies
        :param int timeout: default=5, if the page doesn't load in time, upper this value
        :param arr proxyList: your array of proxies. ip:port:user:pw
        """
        self.__twitterHandle = twitterHandle
        self.__chromedriverPath = chromedriverPath
        self.__accCookies = cookies
        self.__timeout = timeout

        # format proxy
        self.__proxyCounter = 0
        if proxyList != "" and proxyList != None:
            self.proxies = []
            for proxy in proxyList:
                __split = str(proxy).replace("\n", "").split(":")
                fProxy = {'https': f'http://{__split[2]}:{__split[3]}@{__split[0]}:{__split[1]}'}
                self.proxies.append(fProxy)
        else:
            self.proxies = None
            
            
        # convert handle to id [{"handle": handle, "id": id]}]
        self.__multipleHandles = False
        if isinstance(twitterHandle, list) and len(twitterHandle) > 1:
            self.__multipleHandles = True
            print("converting twitter-ids", end=" ")
            retries = 0
            while retries < 5:
                try:
                    self._IDList = asyncio.run(self.__getTwitterIDs())
                    break
                except Exception as e:
                    #print(traceback.format_exc())
                    retries = retries + 1
            print("- done")
                

        # get all the important data to send a request
        __twitterData = self.getTwitterGuestData(cookies=cookies)
        self.__headers = __twitterData[0]
        self.__headersDict = __twitterData[1]
        self.__cookies = __twitterData[2]
        self.__reqUrl = __twitterData[3]
        self.__userID = __twitterData[4]

        self.__session = requests.session()
        e2 = 0
        while e2 < 5:
            try:
                self.__openingResp = self.__session.get(url=self.__reqUrl, headers=self.__headers, cookies=self.__cookies, proxies=self.changeProxy())
                break
            except:
                #print(traceback.format_exc())
                print("failed openingResp. Trying again with new proxy")
                e2 = e2 + 1
                self.__proxyCounter = self.__proxyCounter + 1
                __twitterData = self.getTwitterGuestData(cookies=self.__accCookies)
                self.__headers = __twitterData[0]
                self.__headersDict = __twitterData[1]
                self.__cookies = __twitterData[2]

        self.__openingResp = self.__openingResp.json()  # may raise a JsonDecodeError when you get ratelimited
        self.__userResp = \
        self.__openingResp['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][0]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']


    async def __getID(self, handle):
        headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        async with aiohttp.ClientSession() as s:
            text = "error-co"
            data = None
            while text == "error-co":
                async with s.post(url="https://tweeterid.com/ajax.php", headers=headers, data=f"input={handle}") as resp:
                    text = await resp.text()
                    if text != "error-co":
                        data = {"handle": handle, "id": text}
                    else:
                        time.sleep(0.05)
            return data

    async def __getTwitterIDs(self):
            coroutines = []
            for handle in self.__twitterHandle:
                coroutines.append(self.__getID(handle))
            info = await asyncio.gather(*coroutines)
            return info
                    
      
    def getTwitterGuestData(self, cookies, proxySupport=False):
        if proxySupport:
            wireOptions = {
                'proxy': self.proxies
            }
        else:
            wireOptions = None

        print("gathering meta-information")
        # get driver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(self.__chromedriverPath, options=options) #headless
        #driver = webdriver.Chrome(self.__chromedriverPath, seleniumwire_options=wireOptions, options=options) #headless, proxy
        #driver = webdriver.Chrome(self.__chromedriverPath) #window


        if self.__multipleHandles:
            driver.get(f"https://twitter.com/{self.__twitterHandle[0]}")
        else:
            driver.get(f"https://twitter.com/{self.__twitterHandle}")
        #time.sleep(self.__timeout)  # sleep to let the twitter page load

        headersDict = {}
        for headerReq in driver.requests:
            url = headerReq.url
            if "UserTweets" in url and "cursor" not in url:
                reqUrl = url
                userID = url.split("userId%22%3A%22")[1].split("%22%2C%22count%22")[0]
                headersDict = dict(headerReq.headers)
        time.sleep(1)
        driver.close()
        
        headers = {
            'authorization': headersDict['authorization'],
            'cookie': headersDict['cookie'],
            'user-agent': headersDict['user-agent'],
            'x-csrf-token': headersDict['x-csrf-token'],
            'x-guest-token': headersDict['x-guest-token']
        }

        
        # check for cookies
        if cookies != "":
            # get dummy URL to set cookies
            driver.get("https://twitter.com")
            cookies = self.cookieDict(cookies)
            for key, value in cookies.items():
                driver.add_cookie({'name': key, 'value': value, "domain": ".twitter.com"})
        else:
            cookies = self.cookieDict(headersDict['cookie'])
        print("Done!")


        return headers, headersDict, cookies, reqUrl, userID

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
    
    # get Tweet data multiple Accs
    async def __getTweetsPlainAsync(self, handle, id):
        e1 = 0
        while e1 < 5:
            try:
                urlTwitter = f"https://api.twitter.com/graphql/CkON7wJrKLwEVV59ClcmjA/UserTweets?variables=%7B%22userId%22%3A%22{id}%22%2C%22count%22%3A40%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22longform_notetweets_richtext_consumption_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                async with aiohttp.ClientSession() as s:
                    async with s.get(urlTwitter, headers=self.__headers) as resp:
                        data = await resp.json()
                        data = {"handle": handle, "id": id, "resp": data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']}
                break
            except:
                print(traceback.format_exc())
                print("failed to scrape tweets. Trying again with new data")
                e1 = e1 + 1
                self.__proxyCounter = self.__proxyCounter + 1
                __twitterData = self.getTwitterGuestData(cookies=self.__accCookies)
                self.__headers = __twitterData[0]
                self.__headersDict = __twitterData[1]
                self.__cookies = __twitterData[2]
        return data
    
    
    async def __getTweetsPlainMain(self):
        coroutines = []
        for data in self._IDList:
            coroutines.append(self.__getTweetsPlainAsync(data['handle'], data['id']))
        info = await asyncio.gather(*coroutines)
        return info
    
    def getTweetsPlainMultiple(self):
        """
        get all (unfiltered) tweets from every account in your handle list (unnecessary data and ads included)
        
        call with asyncio.run(scraper.getTweetsPlainMultiple())
        """
        resp = asyncio.run(self.__getTweetsPlainMain())
        return resp
    
    def getTweetsTextMultiple(self):
        """
        get text from all tweets from every account in your handle list
        """
        resp = asyncio.run(self.__getTweetsPlainMain())
    
        accountTweets = []
        for handle in resp:
            tweets = []
            for tweet in handle['resp']:
                if "promotedTweet" not in tweet['entryId']:
                    try:
                        tweets.append({
                            'entryId': tweet['entryId'],
                            'retweet': self.getRetweetInfo(tweet),
                            'text': tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text']})
                    except:
                        continue
            accountTweets.append({
                "handle": handle['handle'],
                "id": handle['id'],
                "tweets": tweets
            })
        return accountTweets
    
    

    # get Tweet data
        
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

    def getTweetsPlain(self):
        """
        get all (unfiltered) tweets from an account (unnecessary data included)
        """
        e1 = 0
        while e1 < 5:
            try:
                resp = self.__session.get(url=self.__reqUrl, headers=self.__headers, cookies=self.__cookies, proxies=self.changeProxy())
                jresp = resp.json()['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']
                break
            except:
                #print(traceback.format_exc())
                print("failed to scrape tweets. Trying again with new data")
                e1 = e1 + 1
                self.__proxyCounter = self.__proxyCounter + 1
                __twitterData = self.getTwitterGuestData(cookies=self.__accCookies)
                self.__headers = __twitterData[0]
                self.__headersDict = __twitterData[1]
                self.__cookies = __twitterData[2]
        return jresp

    def getTweetsText(self):
        """
        get text from all tweets from an account
        """
        resp = self.getTweetsPlain()
        tweets = []
        for tweet in resp:
            if "promotedTweet" not in tweet['entryId']:
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
        return \
        self.__openingResp['data']['user']['result']['timeline_v2']['timeline']['instructions'][2]['entry']['content']['itemContent']['tweet_results']['result']

    # get User data
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
        returns the id of an account
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

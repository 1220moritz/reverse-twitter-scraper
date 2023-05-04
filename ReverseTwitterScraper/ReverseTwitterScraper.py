import time
import traceback

import asyncio
import httpx
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options


class TwitterScraper:

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
        if type(self.proxies) is list and self.__proxyCounter < len(self.proxies) - 1:    #change to next proxy in list
            return self.proxies[self.__proxyCounter]
        elif type(self.proxies) is list and self.__proxyCounter >= len(self.proxies) - 1: # restart with first proxy in list
            self.__proxyCounter = 0
            return self.proxies[self.__proxyCounter]
        else:
            return None
        
    def __init__(self, twitterHandle: list, chromedriverPath: str, cookies="", proxyList=""):
        """
        makes everything ready to scrape twitter.

        :param list twitterHandle: e.g. https://twitter.com/elonmusk -> handle = [elonmusk] or multiple handles ["elonmusk", "POTUS", "BitcoinMagazine"]
        :param str chromedriverPath: e.g. C:/Program Files (x86)/chromedriver.exe
        :param str cookies: your twitter account cookies
        :param arr proxyList: your array of proxies. ip:port:user:pw
        """
        self.__twitterHandle = twitterHandle
        self.__chromedriverPath = chromedriverPath
        self.__accCookies = cookies

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
        if isinstance(twitterHandle, list):
            print("converting twitter-ids", end=" ")
            retries = 0
            while retries < 5:
                try:
                    self._IDList = asyncio.run(self.__getTwitterIDs())
                    break
                except Exception as e:
                    print(traceback.format_exc())
                    retries = retries + 1
            print("- done")
        else:
            raise Exception("twitterHandle must be a list of handles")
                

        # get all the important data to send a request
        retries = 0
        while retries < 5:
            try:
                self.getTwitterGuestData(cookies=cookies)
                break
            except:
                #print(traceback.format_exc())
                retries += 1
                self.__proxyCounter += 1
            
        retries = 0
        while retries < 5:
            try:
                self.__openingResp = httpx.get(url=self.__reqUrl, headers=self.__headers, cookies=self.__cookies).json()
                self.__userResp = self.__openingResp['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][0]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']
                break
            except:
                #print(traceback.format_exc())
                print("failed openingResp. Trying again with new proxy")
                retries += 1
                self.__proxyCounter += 1
                self.getTwitterGuestData(cookies=self.__accCookies)

    async def __getID(self, client: httpx.Client, handle):
        headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        text = "error-co"
        data = None
        while text == "error-co":
            resp = await client.post(url="https://tweeterid.com/ajax.php", headers=headers, data=f"input={handle}")
            text = resp.text
            if text != "error-co":
                data = {"handle": handle, "id": text}
            else:
                await asyncio.sleep(0.05)
        return data

    async def __getTwitterIDs(self):
        async with httpx.AsyncClient() as client:
            coroutines = []
            for handle in self.__twitterHandle:
                coroutines.append(self.__getID(client, handle))
            info = await asyncio.gather(*coroutines)
            await client.aclose()
            return info
 
    def getTwitterGuestData(self, cookies):
        print("gathering meta-information")
        self.__resetData() #clear old data
            
        # get driver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(self.__chromedriverPath, options=options) #headless
        #driver = webdriver.Chrome(self.__chromedriverPath) #window
    
    
        driver.get(f"https://twitter.com/{self.__twitterHandle[0]}")
        #time.sleep(self.__timeout)  # sleep to let the twitter page load
        
        
        headersDict = {}
        for headerReq in driver.requests:
            url = headerReq.url
            if "UserTweets" in url and "cursor" not in url:
                self.__reqUrl = url
                headersDict = dict(headerReq.headers)
        time.sleep(1)
        
        driver.close()
        
        self.__headers = {
            'authorization': headersDict['authorization'],
            'cookie': headersDict['cookie'],
            'user-agent': headersDict['user-agent'],
            'x-csrf-token': headersDict['x-csrf-token'],
            'x-guest-token': headersDict['x-guest-token']
        }

        
        # check for cookies
        if cookies != "":
            self.__cookies = self.cookieDict(cookies)
        else:
            self.__cookies = self.cookieDict(headersDict['cookie'])
        print("Done!")

    def __resetData(self):
        self.__headers = None
        self.__openingResp = None
        self.__userResp = None
        self.__reqUrl = None
        self.__cookies = None
  
    
    
    
    
    # get Twitter data methodes
    ## get user data
    async def __getUserPlainAsync(self, client: httpx.AsyncClient, handle, id):
        retries = 0
        while retries < 5:
            try:
                urlTwitter = f"https://api.twitter.com/graphql/CkON7wJrKLwEVV59ClcmjA/UserTweets?variables=%7B%22userId%22%3A%22{id}%22%2C%22count%22%3A40%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22longform_notetweets_richtext_consumption_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                resp = await client.get(urlTwitter, headers=self.__headers)
                data = resp.json()
                data = {"handle": handle, "id": id, "resp": data}
                break
            except Exception as e:
                raise Exception(e)
        return data
    
    
    async def __getUserPlainMain(self):
        try:
            async with httpx.AsyncClient(proxies=self.changeProxy()) as client:
                coroutines = []
                for data in self._IDList:
                    coroutines.append(self.__getUserPlainAsync(client, data['handle'], data['id']))
                info = await asyncio.gather(*coroutines)
        except Exception as e:
                raise Exception(e)
        return info
    
    def getUserPlain(self):
        """
        get all (unfiltered) data from every account in your handle list ("unnecessary" data and ads included)
        
        :return: [{"handle": handle1, "id": id1, "resp": data1}, {"handle": handle2, "id": id2, "resp": data2},]
        """
        retries = 0
        while retries < 5:
            try:
                resp = asyncio.run(self.__getUserPlainMain())
                break
            except:
                #print(traceback.format_exc())
                print("failed to scrape tweets. Trying again with new data")
                retries += 1
                self.__proxyCounter += 1
                self.getTwitterGuestData(cookies=self.__accCookies)
                
        return resp
    
    ## get twitter data
    async def __getTweetsPlainAsync(self, client: httpx.AsyncClient, handle, id):
        retries = 0
        while retries < 5:
            try:
                urlTwitter = f"https://api.twitter.com/graphql/CkON7wJrKLwEVV59ClcmjA/UserTweets?variables=%7B%22userId%22%3A%22{id}%22%2C%22count%22%3A40%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22longform_notetweets_richtext_consumption_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
                resp = await client.get(urlTwitter, headers=self.__headers)
                data = resp.json()
                data = {"handle": handle, "id": id, "resp": data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']}
                break
            except Exception as e:
                raise Exception(e)
        return data
    
    
    async def __getTweetsPlainMain(self):
        try:
            async with httpx.AsyncClient(proxies=self.changeProxy()) as client:
                coroutines = []
                for data in self._IDList:
                    coroutines.append(self.__getTweetsPlainAsync(client, data['handle'], data['id']))
                info = await asyncio.gather(*coroutines)
        except Exception as e:
                raise Exception(e)
        return info
    
    def getTweetsPlain(self):
        """
        get all (unfiltered) tweets from every account in your handle list (unnecessary data and ads included)
        
        :return: [{"handle": handle1, "id": id1, "resp": {1}}, {"handle": handle2, "id": id2, "resp": {2}}]
        """
        retries = 0
        while retries < 5:
            try:
                resp = asyncio.run(self.__getTweetsPlainMain())
                break
            except:
                #print(traceback.format_exc())
                print("failed to scrape tweets. Trying again with new data")
                retries += 1
                self.__proxyCounter += 1
                self.getTwitterGuestData(cookies=self.__accCookies)
                
        return resp

    def getTweetsText(self):
        """
        get text from all tweets from every account in your handle list
        
        :return: [{'entryId': entryId1, 'retweet': retweet1, 'text': text1}, {'entryId': entryId2, 'retweet': retweet2, 'text': text2}]
        """
        retries = 0
        while retries < 5:
            try:
                resp = asyncio.run(self.__getTweetsPlainMain())
                break
            except:
                #print(traceback.format_exc())
                print("failed to scrape tweets. Trying again with new data")
                retries += 1
                self.__proxyCounter += 1
                self.getTwitterGuestData(cookies=self.__accCookies)
    
        accountTweets = []
        for handle in resp:
            tweets = []
            for tweet in handle['resp']:
                if "promotedTweet" not in tweet['entryId']:
                    try:
                        tweets.append({
                            'entryId': tweet['entryId'],
                            'retweet': self.filterRetweetInfo(tweet),
                            'text': tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text']})
                    except:
                        continue
            accountTweets.append({
                "handle": handle['handle'],
                "id": handle['id'],
                "tweets": tweets
            })
        return accountTweets
  
    
    
    
    
    # filter methodes
    ## filter Tweet data
    def filterRetweetInfo(self, singlePlainTweet, getRetweetInfo=False):
        """
        checks if the tweet is a retweet (returns True, False or the TweetInfo (if you use getRetweetInfo=True))

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        :param getRetweetInfo: default=False -> get all info about the retweetet tweet
        """

        if 'retweeted_status_result' in singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']:
            if getRetweetInfo:
                return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['retweeted_status_result']
            else:
                return True
        else:
            return False
        
    def filterTweetCreatedAt(self, singlePlainTweet):
        """
        returns creation date of a tweet

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['created_at']

    def filterTweetID(self, singlePlainTweet):
        """
        returns the ID of a tweet

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['id_str']

    def filterRetweetCount(self, singlePlainTweet):
        """
        returns how many times the tweet has been retweeted

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count']

    def filterReplyCount(self, singlePlainTweet):
        """
        returns how many replies the tweet has

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['legacy']['reply_count']

    def filterViews(self, singlePlainTweet):
        """
        returns how many views the tweet has

        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        """
        return singlePlainTweet['content']['itemContent']['tweet_results']['result']['views']['count']

    ## filter Account data
    def __defaultAccountFilter(self, singleUserPlain):
        return singleUserPlain['resp']['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][0]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']
    
    def filterPinnedTweetInfo(self, singleUserPlain):
        """
        returns all (unfiltered) information about the pinned tweet of an Account
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return singleUserPlain['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][0]['content']['itemContent']['tweet_results']['result']
        
    def filterIsBusinessAccount(self, singleUserPlain):
        """
        returns if the account is a business account
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return self.__defaultAccountFilter(singleUserPlain)['business_account']

    def filterUserID(self, singleUserPlain):
        """
        returns the id of an account
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return self.__defaultAccountFilter(singleUserPlain)['id']

    def filterIsBlueVerified(self, singleUserPlain):
        """
        returns if the account is verified with a twitter blue check
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return self.__defaultAccountFilter(singleUserPlain)['is_blue_verified']

    def filterAccountCreationDate(self, singleUserPlain):
        """
        returns the creation time of an account
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return self.__defaultAccountFilter(singleUserPlain)['legacy']['created_at']

    def filterDescription(self, singleUserPlain):
        """
        returns the description of an account
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return self.__defaultAccountFilter(singleUserPlain)['legacy']['description']

    def getUserSpecificData(self, singleUserPlain):
        """
        returns all (unfiltered) data about an account
        
        :param getUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info
        """
        return self.__defaultAccountFilter(singleUserPlain)

# ReverseTwitterScraper
ReverseTwitterScraper is a Python package that provides an easy-to-use tool for scraping tweets of a single or multiple Twitter accounts. This package uses Selenium and httpx to scrape tweets and other account data.

## Links
GitHub: https://github.com/1220moritz/reverse-twitter-scraper  
PyPI: https://pypi.org/project/ReverseTwitterScraper/

## Installation
To install the package, simply run the following command:
```
pip install ReverseTwitterScraper
```

## Usage
To use this package, you need to follow these steps:

1. Import the TwitterScraper class from the package.  
2. Create an object of the TwitterScraper class.  
3. Call any method of the TwitterScraper class.  

Here's an example code:
```
from ReverseTwitterScraper import TwitterScraper

chromedriver_path = "C:/Program Files (x86)/chromedriver.exe"
cookies = "" #no account cookies
cookies = {'Cookie': 'your Cookie', 'X-Csrf-Token': 'your csrf token'} #with account cookie
proxy_list = []


twitter_handle = ["elonmusk"]  # single account
twitter_handles = ["elonmusk", "POTUS", "latestinspace"]  # multiple accounts
scraper = TwitterScraper(twitter_handle, chromedriver_path, cookies, proxy_list)
tweets = scraper.getTweetsText()

print(tweets)
```

In the above code, we first import the TwitterScraper class from the package. Then, we create an object of the TwitterScraper class with the required parameters.
Finally, we call the getTweetsText() method to get the tweets of the specified Twitter account.

## Parameters
The TwitterScraper class takes the following parameters:

- twitterHandle: The Twitter handle of the account(s) to be scraped. For example, if the account URL is https://twitter.com/elonmusk, then the twitterHandle parameter should be set to ['elonmusk'].

- chromedriverPath: The path of the Chrome driver executable file. This file is required to use the Selenium module.

- cookies: (Optional) The cookies of a logged-in Twitter account. If you have a Twitter account and want to scrape tweets that are not publicly available, you can pass the cookies of your logged-in account.

- proxyList: (Optional) A list of proxies to use for scraping. The list should contain proxy addresses in the format ip:port:user:pw.


## How to get account cookies:
Following a private "target" account is necessary to access its data. Then, account cookies can be used to scrape the account.
1. Open the Chrome browser and go to the Twitter website.
2. If you're not already logged in, log in to your Twitter account.
3. Right-click anywhere on the page and select "Inspect" from the context menu. Alternatively, you can press "Ctrl+Shift+I" (Windows) or "Cmd+Option+I" (Mac) on your keyboard.
4. This will open the Developer Tools pane. Click on the "Network" tab at the top and then filter with fetch/XHR.
5. On the left-hand sidebar, click on any request.
6. You should now see a list of metadata associated with this specific request. Look for the "Request Headers" section and then find the "cookies" entry. Copy the entire value of the cookies.
7. In your Python code, create a new instance of the TwitterScraper class and paste the cookie value as the value of the "cookies" parameter.
8. That's it! You can now use the TwitterScraper class to scrape data from your Twitter account.  

By following these steps, you should be able to retrieve the necessary cookies from your Twitter account and use them in your Python code to scrape data.

## Methodes:

## get twitter data
### getUserPlain()
      get all (unfiltered) data from every account in your handle list ("unnecessary" data and ads included)
      returns [{"handle": handle1, "id": id1, "resp": data1}, {"handle": handle2, "id": id2, "resp": data2},]

### getTweetsPlain()
      get all (unfiltered) tweets from every account in your handle list (unnecessary data and ads included)
      returns [{"handle": handle1, "id": id1, "resp": {1}}, {"handle": handle2, "id": id2, "resp": {2}}]
     
### getTweetsText()
      get text from all tweets from every account in your handle list
      returns [{'entryId': entryId1, 'retweet': retweet1, 'text': text1}, {'entryId': entryId2, 'retweet': retweet2, 'text': text2}]


## filter Tweet data
### filterRetweetInfo(singlePlainTweet, getRetweetInfo=False):
        checks if the tweet is a retweet (returns True, False or the TweetInfo (if you use getRetweetInfo=True))
        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info
        :param getRetweetInfo: default=False -> get all info about the retweetet tweet
      
### filterTweetCreatedAt(singlePlainTweet)
    returns createTimeDate of a tweet
    :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info

### filterTweetID(singlePlainTweet)
        returns the ID of a tweet
        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info

### filterRetweetCount(singlePlainTweet)
        returns how many times the tweet has been retweeted
        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info

### filterReplyCount( singlePlainTweet)
        returns how many replies the tweet has
        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info

### filterViews(singlePlainTweet)
        returns how many views the tweet has
        :param singlePlainTweet: plain (unfiltered) info of a tweet. Use getTweetsPlain() to get the info


## filter Account data
### filterPinnedTweetInfo(singleUserPlain)
        returns all (unfiltered) information about the pinned tweet
		:param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

### filterIsBusinessAccount(singleUserPlain)
        returns if the account is a business account
        :param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

### filterUserID(singleUserPlain)
        returns the id of an account
        :param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

### filterIsBlueVerified(singleUserPlain)
        returns if the account is verified with a twitter blue check
        :param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

### filterAccountCreationDate(singleUserPlain)
        returns the creation time of an account
        :param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

### filterDescription(singleUserPlain)
        returns the description of an account
        :param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

### getUserSpecificData(singleUserPlain)
        returns all (unfiltered) data about an account
        :param singleUserPlain: plain (unfiltered) info of a Twitter account. Use getUserPlain() to get the info

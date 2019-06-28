import asyncio
from pyppeteer import launch


async def main():
    # declare headless=True to make it not show the scraping
    browser = await launch(headless=True)
    page = await browser.newPage()
    #go to twitter page of choosing (Donald Trump here)
    await page.goto('https://twitter.com/realDonaldTrump')
    #set time to wait
    await asyncio.sleep(1)
    #set how much it should scrape
    pages = 10
    #scroll though the Twitter
    for i in range(pages):
        await page.evaluate('() => window.scrollTo(0,document.body.scrollHeight)')
        await asyncio.sleep(1)
    #get the content of each tweet "block"
    tweets = await page.xpath('//ol[@id="stream-items-id"]//div[@class="content"]')
    #create list to store data
    tweet_data = []
    #for loop iterating over every tweet "block"
    for elem in tweets:
        #find fullname
        title = await elem.xpath('.//strong[contains(@class, "fullname")]')
        #find comments class
        comments = await elem.xpath('.//button[contains(@class, "js-actionReply")]//span[@class="ProfileTweet-actionCountForPresentation"]')
        #find retweets class
        retweets = await elem.xpath('.//button[contains(@class, "js-actionRetweet")]//span[@class="ProfileTweet-actionCountForPresentation"]')
        #find likes class
        likes = await elem.xpath('.//button[contains(@class, "js-actionFavorite")]//span[@class="ProfileTweet-actionCountForPresentation"]')
        #find value of name
        name_value = await page.evaluate('(elem) => elem.innerHTML', title[0])
        #find number of comments
        comment_count = await page.evaluate('(elem) => elem.innerHTML', comments[0])
        #find number of retweets
        retweet_count = await page.evaluate('(elem) => elem.innerHTML', retweets[0])
        #find number of likes
        like_count = await page.evaluate('(elem) => elem.innerHTML', likes[0])
        #store data in the list
        tweet_data.append((name_value, comment_count, retweet_count, like_count))
    #print data to console
    print(tweet_data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())


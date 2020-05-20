import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from progress.bar import IncrementalBar
# import jupyter
import random
import urllib3
import datetime




print('working folder is ' + str(os.getcwd()))

print('website loading...')
driver = webdriver.Firefox()
url = u'https://twitter.com/f1debrief'
print('website loaded, minimizing browser window')
driver.get(url)
time.sleep(1)
driver.minimize_window()

"""
http = urllib3.PoolManager()
response = http.request('GET', url)
soup = BeautifulSoup(response.data)

soup_tweets = soup.find_all('li', 'js-stream-item')
for soup_tweet in soup_tweets:
    if soup_tweet.find('p', 'tweet-text'):
        timestamp = soup_tweet.find('a', 'tweet-timestamp')['title']
        tweet_timestamp = datetime.datetime.strptime(timestamp, '%H:%M - %d %b %Y')
    else:
        continue
"""
# move mouse and click to activate page scroll
canopy = driver.find_element_by_class_name('ProfileCanopy-header')
body = driver.find_element_by_tag_name('body')

hover_mouse = ActionChains(driver).move_to_element(canopy)
hover_mouse.perform()
canopy.click()


def site_scroll_progress_bar_progress(scroll_amount):
    page_down = 0
    page_down_count = scroll_amount
    page_bar = IncrementalBar('Loading twitter pages', max=scroll_amount)

    for r in range(page_down_count):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        page_down += 1
        page_bar.next()
    page_bar.finish()


tweet_need = int(input('Tweet pages to analyze: '))
site_scroll_progress_bar_progress(int(tweet_need))

tweet_list = driver.find_elements_by_class_name('tweet-text')
# tweet_times_list = tweet.find('a', 'tweet-timestamp')['title']
# tweet_times_list = driver.find_elements_by_xpath(
# [element.get_attribute('title') for element in driver.
# find_elements_by_xpath('//a[starts-with(@class, "tweet-timestamp
# js-permalink js-nav js-tooltip")]')])
tweet_count = len(tweet_list)

print('Tweet count: ' + str(tweet_count))
sample_tweet = random.randint(0, tweet_count + 1)
print('\nSample tweet:\n ' + str(tweet_list[sample_tweet].text) + '\n')

data_list = []
time_list = []
print('creating data...')

tweet_dataframe = pd.DataFrame([])
date_dataframe = pd.DataFrame([])
date_list = []
bar = IncrementalBar('Tweets added to db:', max=len(tweet_list))

# web element's text is added to the list and that list is added to dataframe

for tweet in tweet_list:
    txt = tweet.text
    split_txt = txt.splitlines()
    data_list.append(split_txt)

    # tweet.('a', 'tweet-timestamp')['title']

    tweet_dataframe = pd.DataFrame(data_list)
    bar.next()
bar.finish()
tweet_dates = [element.get_attribute('title') for element in driver.find_elements_by_xpath('//a[starts-with(@class, "tweet-timestamp js-permalink js-nav js-tooltip")]')]
# print(tweet_dates)

date_list.append(tweet_dates)

# split_date_list = date_list.

date_column = pd.Series(date_list)

tweet_dataframe[0] = date_list

# tweet_dataframe['Date'] = date_column
# tweet_dataframe.insert(loc=0, column='Date', value=date_column)

"""
bar = IncrementalBar('Timestamps added to db:', max=len(time_list))
for times in tweet_times_list:
    time_list_txt = tweet_times_list.text
    split_timestamp_list = time_list_txt.splitlines()
    time_list.append(split_timestamp_list)
    dt = pd.DataFrame(time_list)
    bar.next()
bar.finish()
"""
print('created Dataframe')

time_str = str(time.strftime('%y-%m-%d_%H-%M-%S'))
csv_filename = 'twitter_f1debrief'
tweet_dataframe_name = r'~/' + time_str + csv_filename + '_' + str(tweet_count) + '_tweets' + '.csv'
tweet_dataframe.to_csv(tweet_dataframe_name)
print('written file to ' + tweet_dataframe_name)
"""
date_dataframe_filename = r'~/' + time_str + csv_filename + '_' + str(tweet_count) + '_timestamps' + '.csv'
date_dataframe.to_csv(date_dataframe_filename)
print('written file to ' + date_dataframe_filename)
"""
print('Quit browser')
driver.quit()

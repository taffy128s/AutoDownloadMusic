# -*- coding: utf-8 -*-

import time, urllib2, sys
import lxml.html as lh
from selenium import webdriver

song_list = []
with open('song_list') as f:
    song_list = f.readlines()

for song in song_list:
    googleDriver = webdriver.Firefox(executable_path = '/Users/taffy128s/Documents/geckodriver')
    googleDriver.get('https://www.google.com#q=' + song)
    link = ''
    count = 0
    while link is '':
        try:
            link = googleDriver.find_elements_by_tag_name('cite')[count].text
            if ('youtube' in link) is False:
                link = ''
                count += 1
        except:
            pass
    googleDriver.close()

    converterDriver = webdriver.Firefox(executable_path = '/Users/taffy128s/Documents/geckodriver')
    converterDriver.get('http://www.youtube-mp3.org/')
    element = converterDriver.find_element_by_id('youtube-url')
    element.clear()
    element.send_keys(link)
    converterDriver.find_element_by_id('submit').click()
    # sleep
    # time.sleep(5)
    # sleep
    down_link = ''
    while down_link is '':
        try:
            down_link = converterDriver.find_element_by_id('dl_link').find_elements_by_tag_name('a')[2].get_attribute('href')
        except:
            pass
    converterDriver.close()
    print 'Downloading ' + song
    while True:
        try:
            req = urllib2.Request(down_link, headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'})
            mp3file = urllib2.urlopen(req)
            with open(song[0 : len(song) - 1] + '.mp3','wb') as output:
                output.write(mp3file.read())
            break
        except Exception as e:
            print e

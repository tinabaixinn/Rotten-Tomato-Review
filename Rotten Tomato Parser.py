#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 22:43:13 2019

@author: baixinwang
"""

import requests # to get the website
import time     # to force our code to wait a little before re-trying to grab a webpage
import re       # to grab the exact element we need
from bs4 import BeautifulSoup # to grab the html elements we need

movie = "a_star_is_born_2018"
pageNum = 5


# create an empty list
data  = [] 
# access the webpage as Chrome
my_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

for k in range(1,pageNum+1):
    
    # Give the url of the page
    page = 'https://rottentomatoes.com/m/'+movie+'/reviews?page='+str(k)
    # Initialize src to be False
    src  = False

    # Now get the page

    # try to scrape 5 times
    for i in range(1,6): 
        try:
            # get url content
            response = requests.get(page, headers = my_headers)
            # get the html content
            src = response.content
            # if we successuflly got the file, break the loop
            break 
        # if requests.get() threw an exception, i.e., the attempt to get the response failed
        except:
            print ('failed attempt #',i)
            # wait 2 secs before trying again
            time.sleep(2)

    # if we could not get the page 
    if not src:
       # couldnt get the page, print that we could not and continue to the next attempt
       print('Could not get page: ', page)
       # move on to the next page
       continue 
    else:
       # got the page, let the user know
       print('Successfully got page: ', page)
    
    soup = BeautifulSoup(src.decode('ascii', 'ignore'), 'lxml')
    reviews = soup.findAll('div', {'class':re.compile('row review_table_row')})

    for review in reviews:

        # initialize to not found
        critic_name = 'NA'
        rating  = 'NA'
        review_source = 'NA'
        review_text = 'NA'
        review_date = 'NA'

        # find a, grab critic name
        a = review.find('a')

        # if you found it
        if a:
            critic_name = a.text

        # find icon, grab critic name
        icon = review.findAll('div', {'class':re.compile('review_icon')})
        
        # if you found it
        if icon:
            rating = icon[0].attrs['class'][-1]
            
        # find em, grab review source
        em = review.find('em')

        # if you found it
        if em:
            review_source = em.text
            
        # find div for review text, grab div's text, strip() it
        div_review_text = review.findAll('div', {'class':re.compile('the_review')})

        # if you found it
        if div_review_text:
            review_text  = div_review_text[0].text.strip()

        # find div for review date, grab div's text, strip() it
        div_review_date = review.findAll('div', {'class':re.compile('review-date')})

        # if you found it
        if div_review_date:
            review_date  = div_review_date[0].text.strip()

        # add all the info to the data link
        # if some element hasn't been found, the 'NA' string will be added
        data.append([critic_name, rating, review_source, review_text, review_date])

with open('baixin_wang_'+movie+'.txt', mode='w', encoding='utf-8') as f:
    for statement in data:
        f.write(statement[0] + '\t' + statement[1] + '\t' + statement[2] + '\t' + statement[3] + '\t' + statement[4] + '\n')
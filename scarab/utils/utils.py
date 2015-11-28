#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Oct 29, 2015 '
__author__= 'samuel'

import BeautifulSoup
import requests
import random


def get_nationalgeographic_image_url():
    return ''
    url = 'http://photography.nationalgeographic.com/photography/photo-of-the-day'
    #r = requests.get(url + '/archive/')
    r = requests.get(url + '/nature-weather/')
    soup = BeautifulSoup.BeautifulSoup(r.text)
    #image_url = random.choice([o.get('src') for o in soup.find('div', {'id':'search_results'}).findAll('img')])
    target_url = random.choice([o.get('href') for o in soup.find('div', {'id':'search_results'}).findAll('a')])
    target_soup = BeautifulSoup.BeautifulSoup(requests.get('http://photography.nationalgeographic.com' + target_url).text)
    image_url = 'http:' + [o.get('src') for o in target_soup.find('div', {'class':'primary_photo'}).findAll('img')][0]
    return image_url


#!/usr/bin/env python3 
from bs4 import BeautifulSoup
from variables.py import nyms, nyms1, nyms2, baseUrl
import requests 
import json
import re

urlArr = []
nextPosts = str('Next ') 
regex = "Next [0-9]{1,2}."

for nym in nyms:
    url = baseUrl + '/search/swish.cgi?query=' + nym + '&metaname=author&sort=unixdate&reverse=on&dr_e_year=2018&dr_s_year=1998&start='
    nextUrl = ''
    # test url 'Next"
    #    url = baseUrl + '/search/swish.cgi?query=Next&metaname=swishtitle&sort=unixdate&reverse=on&dr_s_day=1&dr_o=13&dr_e_year=2018&dr_s_year=1997&dr_e_day=12&dr_s_mon=1&dr_e_mon=10&start=30'

    # test url 'Barbie'
    #    url = baseUrl + '/search/swish.cgi?query=barbie&submit=Search%21&metaname=author&sort=unixdate&reverse=on&dr_o=13&dr_s_mon=1&dr_s_day=1&dr_s_year=1997&dr_e_mon=10&dr_e_day=12&dr_e_year=2018'

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    while nextUrl is not None:
        for link in soup.find_all('a'):
            if link.string and link.string.startswith('Next '):
                nextUrl = baseUrl + link.get('href')
            #    print (link.string)
            #    print (nextUrl)
                break
            elif link.string is None:
                nextUrl = None
                continue

        for link in soup.find_all('dt'):
            link = link.find('a').get('href')
            urlArr.append(link)

        with open('postUrls.json', 'a') as outfile:
            json.dump(urlArr, outfile)
            outfile.write("\n")
            urlArr = []

        response = requests.get(nextUrl, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")



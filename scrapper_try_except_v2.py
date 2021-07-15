# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
from bs4 import BeautifulSoup
import time

elapsed_time = 0

def downloadPDF(urlName,saveName):
    print 'TRYING TO GET: ',urlName
    print 'Going To Save at: ',saveName
    try:
        response = urllib2.urlopen(urlName)
    except:
        try:
            print 'Error fetching'
            time.sleep(305)
            response = urllib2.urlopen(urlName)
        except:
            try:
                print 'Error fetching'
                time.sleep(305)
                response = urllib2.urlopen(urlName)
            except:
                print ' Didnlt Work'

    try:
        file = open(saveName,'wb')
        file.write(response.read())
        file.close()
        print("Completed")
        time.sleep(0.1)
    except:
        print 'Not Saved'


def get_page(url_prefix,page_num,max_page):
    #If we are beyond the maximum pages, return
    if page_num > max_page:
        return

    #Define what page we should be on
    main_url = url_prefix+str(page_num)
    print '******************'
    print main_url
    print '********************'
    page = urllib2.urlopen(main_url)
    url = BeautifulSoup(page)
    records =  url.find_all('form',attrs={'name':'addForm'})[0]

    #print records
    article_links = []
    for a in records.find_all('a', href=True):
        if 'hdl' in a['href']:
            article_links.append(a['href'])

    for item in article_links:
        #Get the paper from the full view link
        get_paper(item)

    #Get the next page
    get_page(url_prefix,page_num+1,max_page)

def get_paper(url):
    prefix = "https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id="
    suffix_1 = ";view=1up;seq=2"
    suffix_2 = ";view=1up;seq=3"

    #Create the PDF url
    url_id = url.split('2027/')[1]
    #Page 2 of PDF
    urlName_1 = prefix+url_id+suffix_1
    #Page 3 of PDF
    urlName_2 = prefix+url_id+suffix_2

    fileName_1 = url_id.replace(':','_').replace('/','_') +'_2'+'.pdf'
    fileName_2 = url_id.replace(':','_').replace('/','_') +'_3'+'.pdf'

    #Download the PDF
    downloadPDF(urlName_1,fileName_1)
    downloadPDF(urlName_2,fileName_2)


def main():
    #access key: 
    # secret key:

    #Start page
    main_url = "https://catalog.hathitrust.org/Search/Home?type%5B%5D=subject&lookfor%5B%5D=architecture&page=1&ft=ft&page=1"
    page = urllib2.urlopen(main_url)
    soup = BeautifulSoup(page)

    #Get the total pages we will go through by looking up the pagination
    paginate = soup.find_all('div',attrs={'class':'pagination clearfix'})[0]
    pages = []
    #List all the paginations
    for item in paginate.find_all('a',title=True):
        pages.append(item)
    #Get the last pagination (this is our 'last page')
    pages = pages[len(pages)-1]
    #Parse it to get the url, which has the final page number
    last_page = pages['href'].split('=')
    last_page = last_page[len(last_page)-1]
    print last_page

    url_prefix = "https://catalog.hathitrust.org/Search/Home?type%5B%5D=subject&lookfor%5B%5D=architecture&page=1&ft=ft&page="
    max_page = int(last_page)
    start_page = 1
    get_page(url_prefix,start_page,max_page)

    return


main()

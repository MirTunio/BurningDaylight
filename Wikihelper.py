"""
TUNIO 2019
Build out basic wikipedia interface
"""

import wikipedia
from re import sub 
import PyDictionary
dictionary = PyDictionary.PyDictionary()
import pprint
#import requests
#from bs4 import BeautifulSoup

wikipedia.set_lang('en')
page_summary_splits = ''
counter = 1

def wiki(fulltext):
    tokens = fulltext.split(' ')    
    response = ''
    global page_summary_splits
    global counter
    
    if tokens[0].lower() == 'search':
        print('got a search')
        search_term = fulltext[7:]
        search_result = wikipedia.search(search_term)
        search5 = search_result[:5]
        [response + ', ' + result for result in search5][2:]
        response = ", ".join(search5)
        response = response[:150]
        if response == '':
            response = "No entries found!"
        ###print(search_term, response)
        
    elif tokens[0].lower() == 'wiki':
        print('got a wiki') 
        counter = 1
        page_title = sub(' +', ' ', fulltext[4:].rstrip().lstrip())
        try: 
            page_summary_full = wikipedia.summary(page_title)
            if page_summary_full == '':
                response = "This page does not exist, try using english by replying: english, or try using 'search' and replying with correct spelling..."
                return response
            nchars = 300
            page_summary_splits = [page_summary_full[i:i+nchars] for i in range(0,len(page_summary_full),nchars)]
            response = 'PART 1 of {}: '.format(str(len(page_summary_splits))) + page_summary_splits[0]+'... [reply: "more"]'
        except wikipedia.PageError:
            response = "This page does not exist, try using 'search' and replying with correct spelling..."
        ###print(page_title, response)
        
    elif tokens[0].lower().rstrip().lstrip() == 'more': 
        if counter >= len(page_summary_splits):
            response = "END OF SUMMARY..."
        else:
            response = 'PART {} of {}: '.format(str(counter+1),str(len(page_summary_splits))) + page_summary_splits[counter] +'...'
            counter += 1
        
    elif tokens[0].lower() == 'about':
        response = "Welcome to Wikipedia SMS, created by TUNIO 2019"
        
    elif tokens[0].lower().rstrip().lstrip() == 'how':
        response = "to set language to urdu, reply: urdu, to set language to english reply: english, to search reply with: search Albert Einstein, to open a page reply with: wiki Albert Einstein, to look up a word in dictionary reply with: define abstraction"
    
    elif tokens[0].lower().rstrip().lstrip() == 'urdu':
        wikipedia.set_lang('ur')
    elif tokens[0].lower().rstrip().lstrip() == 'english':
        wikipedia.set_lang('en')
    
    elif tokens[0].lower().rstrip().lstrip() == 'define':
        word = sub(' +', ' ', fulltext[6:].rstrip().lstrip())
        dictionary_lookup = dictionary.meaning(word)
        pretty_str = pprint.pformat(dictionary_lookup)
        response =  pretty_str
    
    
    else:
        print('got a poor format: ', fulltext)
        response = "poor formatting!, reply with: how"
    return response


# [line[i:i+n] for i in range(0, len(line), n)]
    
#def getSimpleWiki(keyword):
#    # Get simple wiki and return list of 640char buckets
#    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&titles=Stack%20Overflow"
#    simple_url = "https://simple.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&titles=Steve%20Jobs"
#    r = requests.get(url)
#    soup = BeautifulSoup(r.content)
#    # If not, return propper wikipedia page
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
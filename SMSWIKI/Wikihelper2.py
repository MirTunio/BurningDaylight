"""
TUNIO 2019
Build out basic wikipedia and dictionary interface
Now with sessions...
"""

import wikipedia
from re import sub 
import PyDictionary
dictionary = PyDictionary.PyDictionary()
import pprint
import wikiquotes
from bs4 import BeautifulSoup
import requests

#from datetime import date

wikipedia.set_lang('en')
counter = 1

language_holder = {} # contains: "number: language", init with english "en", assert the set language everytime wiki happens
page_summary_holder = {} #sessionID:[fid,page_summary_splits] # will be created/ updated with wiki, used/updated with more

def wiki(fulltext, from_number):
    fulltext = fulltext.rstrip().lstrip()
    response = ''
    global language_holder
    global page_summary_holder
    
    QUERY = fulltext.split(' ')[0].lower().rstrip().lstrip()
    
    if QUERY == 'search': #TODO: NEEDS TO RETURN: RESULTS 1. abcd, 2. asdf, and say: reply with 1 or 2 (etc.) to open wiki page
        print('WIKIHELPER: got a search')
        assert_lang(from_number, override = True)
        search_term = fulltext[7:].lower().rstrip().lstrip() #cuts out the search
        print(search_term)
        search_result = wikipedia.search(search_term) #searches wikipedia with query
        search5 = search_result[:5]
        response = ", ".join(search5)
        response = response[:150] # dont recall why I just look at first 150 chars, but must be important...
        if response == '':
            response = "No entries found!"
        
    elif QUERY == 'wiki':
        assert_lang(from_number)
        print('WIKIHELPER (query): got a wiki')
        page_title = sub(' +', ' ', fulltext[4:].rstrip().lstrip())
        print('WIKIHELPER (page name): ' + page_title)
        try: 
            page_summary_full = wikipedia.summary(page_title)
            if page_summary_full == "":
                response = "This page does not exist, change language to english by replying: english, or try using 'search' and replying with correct spelling..."
                return response   
            
            add_newsplit(from_number, page_summary_full)
            response = 'PART 1 of {}: '.format(str(len(page_summary_holder[from_number][1]))) + page_summary_holder[from_number][1][0]+' [reply: "more"]'
        except wikipedia.PageError:
            response = "This page does not exist, try using 'search' and replying with correct spelling..."
            
    elif QUERY == 'more': 
        if from_number not in page_summary_holder:
            response = "Access a wiki first by using: wiki"
        else:
            RETRIEVED = page_summary_holder[from_number]
            COUNTER_RETRIEVED = RETRIEVED[0]
            SPLIT_RETRIEVED = RETRIEVED[1]
            
            print('WIKIHELPER (query): got a more') 
            if COUNTER_RETRIEVED >= len(SPLIT_RETRIEVED):
                response = "END OF SUMMARY... wiki something new!"
            else:
                response = 'PART {} of {}: '.format(str(COUNTER_RETRIEVED+1),str(len(SPLIT_RETRIEVED))) + SPLIT_RETRIEVED[COUNTER_RETRIEVED] +' [reply: "more"]'
                push_split_counter(from_number)
     
    elif QUERY == 'define':
        word = sub(' +', ' ', fulltext[6:].rstrip().lstrip())
        dictionary_lookup = dictionary.meaning(word)
#        pretty_str = pprint.pformat(dictionary_lookup) #TODO: THIS IS CATEGORICALLYEGORICALLY NOT PRETTY, WHY DO I SEE CURLY BRACKETS??
        pretty_str = ('\n'.join("{}: {}".format(k, v) for k, v in dictionary_lookup.items()))
        response =  pretty_str
           
    elif QUERY == 'urdu': #TODO: Urdu searches VERY VERY strangely sometimes, try wiki WD-40
        language_holder[from_number] = 'ur'
        print("WIKIHELPER: language change to urdu")
        wikipedia.set_lang('ur')
        response = "Language changed to urdu"
        
    elif QUERY == 'english':
        language_holder[from_number] = 'en'
        print("WIKIHELPER: language change to english")
        wikipedia.set_lang('en')
        response = "Language changed to english"
 
    elif QUERY == 'about':
        response = "Welcome to Wikipedia SMS, created by TUNIO 2019"
        
    elif QUERY == 'how':
        response = "to set language to urdu, reply: urdu, to set language to english reply: english, to search reply with: search Albert Einstein, to open a page reply with: wiki Albert Einstein, to look up a word in dictionary reply with: define abstraction. to get quote reply quote of day"
   
    elif QUERY == 'quote':
        QUOTE = wikiquotes.quote_of_the_day("english")
        response = QUOTE[0] + " - " + QUOTE[1]
        
    elif QUERY == 'minariaz':
        QUOTE = wikiquotes.quote_of_the_day("english")
        response = "HEY MINA! HAVE A NICE DAY!! \n\n" + QUOTE[0] + " - " + QUOTE[1] + "\n\ndoggo: \n" + "https://random.dog/" + BeautifulSoup(requests.request("GET","https://random.dog/").text,"lxml").img['src']
        
    else:
        print('WIKIHELPER: got a poor format: ', fulltext)
        response = "poor formatting!, reply with: how"
        
    return response

def assert_lang(from_number, override = False):
    if from_number not in language_holder:
        language_holder[from_number] = 'en'

    if override:
        wikipedia.set_lang('en')
    else:
        desired_language = language_holder[from_number]
        wikipedia.set_lang(desired_language)
        
def add_newsplit(from_number, page_summary_full):   
    nchars = 700
    page_summary_splits = [page_summary_full[i:i+nchars] for i in range(0,len(page_summary_full),nchars)]
    page_summary_holder[from_number] = (1,page_summary_splits)
    
def push_split_counter(from_number):
    OLD = page_summary_holder[from_number]
    NEW = (OLD[0]+1,OLD[1])
    page_summary_holder[from_number] = NEW
     
"""
TUNIO 2019
Build out basic wikipedia and dictionary interface
Now with sessions...
"""

import wikipedia
from re import sub 
import PyDictionary
dictionary = PyDictionary.PyDictionary()
#import wikiquotes
from bs4 import BeautifulSoup
import requests
import DiagnosticTree4

#from datetime import date

wikipedia.set_lang('en')
counter = 1

language_holder = {} # contains: "number: language", init with english "en", assert the set language everytime wiki happens
page_summary_holder = {} #sessionID:[fid,page_summary_splits] # will be created/ updated with wiki, used/updated with more
diagnow = []


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
        response = "To search reply with: search Albert Einstein\nto open a page reply with: wiki Albert Einstein\nto view next part reply with: more\nto set language to urdu reply: urdu\nto set language to english reply: english\nto use dictionary reply with: define abstraction\nto get weather for karachi (beta), reply: weather\nto use sms-diagnosis reply: doctor."
   
#    elif QUERY == 'quote': #Quote library does not work on Termux/Linux flavor. We can figure this out later... 
#        QUOTE = wikiquotes.quote_of_the_day("english")
#        response = QUOTE[0] + " - " + QUOTE[1]
        
    elif QUERY == 'minar': #An easter egg for a friend of mine
        #QUOTE = wikiquotes.quote_of_the_day("english")
        #response = "HEY MINA! HAVE A NICE DAY!! \n\n" + QUOTE[0] + " - " + QUOTE[1] + "\n\ndoggo: \n" + "https://random.dog/" + BeautifulSoup(requests.request("GET","https://random.dog/").text,"lxml").img['src']
        response = "HEY MINA! HAVE A NICE DAY!! \n\ndoggo: \n" + "https://random.dog/" + BeautifulSoup(requests.request("GET","https://random.dog/").text,"html.parser").img['src']
        
    elif QUERY == 'weather':
        #tm@g, weather123
        #what city? #this will need to built out with particular cites, potentailly move to new module...
        #https://openweathermap.org/current
        ID = "1174867" #KARACHI
        OWM = "b958a659ef18989bda00a932f1e9badc"
        URL = "http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}&units=metric".format(ID,OWM)
        jinx = "https://samples.openweathermap.org/data/2.5/forecast?id=524901&appid=b958a659ef18989bda00a932f1e9badc"
        weather_out = requests.request("GET",URL).json() #API key not working yet, tm@gma, weather123, see
        day_list = weather_out['list']
        day_temp = [str((daycast['dt_txt'], daycast['main']['temp'], daycast['weather'][0]['description'])) for daycast in day_list]
        #print(day_temp)
        #Now once key starts working, cull this to next 5 days, temp/rain/etc.
        #It is 5 days, every 3 hrs forecast.
        response = "Forecast for Karachi:\n{}".format('\n'.join(day_temp))
        
        
    elif QUERY == 'doctor' or QUERY == 'diagnose' or QUERY == 'followup' or from_number in diagnow:
        if from_number not in diagnow:
            diagnow.append(from_number)    
        
        response = DiagnosticTree4.qa(fulltext, from_number)
        if 'TUNIO2019' in response:
            diagnow.remove(from_number)
        return response
        
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
    nchars = 600
    page_summary_splits = [page_summary_full[i:i+nchars] for i in range(0,len(page_summary_full),nchars)]
    page_summary_holder[from_number] = (1,page_summary_splits)
    
def push_split_counter(from_number):
    OLD = page_summary_holder[from_number]
    NEW = (OLD[0]+1,OLD[1])
    page_summary_holder[from_number] = NEW
     
    
#%% Notes:
"""
Make each command: 'wiki page', 'wiki how', 'wiki english' etc. etc. So that only those 
messages with 'wiki' infront of them receive a response. But Flask doesn't like empty
returns, hmm. OH RIGHT, the function just returns nothing. Just return nothing. Just don't
do anything. And this check could happen on Envaya level perhaps.. to be seen

Need to add battery and connectivity checks, and then send warnings to HANDLER phone number

GEOLOCATION, THEN:::::
ADD WEATHER FORECASTS!!! NEEED TO DO THISA ASDKJNADWKMAWDMPOW EDO THIS DO THIS DO THIS NOW

Maintain a phonebook
Emergency alerts

ENG/URDU dict. etc. see article Part 3
ENG/SINDHI

Educational courses

Diganosis project (other file)

Need to maintain log on file of past searches, a cache cleared every day or two or something.
^For continuity of 'more', past the breaks in system. And also explicity memory usage monitoring etc.
^^ Save the language holder and page summary holder to pickle or something everytime an authorized 
   shutdown occurs or a 12 hrs pass. load on every start cycle or every save cycle
   
Use Google translate instead of wikipedia Urdu peut-etre....

BUGS:
1) disambiguation pages need to be fixed. (text: wiki pia)
2) Better handling of poorly formatted questions
3) Connect this shit to a Siri/Alexa/Assitant/someone else API

"""
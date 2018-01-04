import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams
import pandas as pd
import string

# FINNEGANS WAKE
wake = open('fulltext.txt',  'r').read() \
        .replace('\n',' ').replace("'", "").replace('.','').replace(',','') \
        .replace('!','').replace(')','').replace('(','').replace(':','') \
        .replace('"','').replace('?','').lower().replace('“','') \
        .replace('—','').replace('-','').replace('”','').replace(';','') \
        .replace('[','').replace(']','').replace('*','')

# CRIME AND PUNISHMENT
crim = open('fulltext2.txt', 'r').read() \
        .replace('\n',' ').replace("'", "").replace('.','').replace(',','') \
        .replace('!','').replace(')','').replace('(','').replace(':','') \
        .replace('"','').replace('?','').lower().replace('“','') \
        .replace('—','').replace('-','').replace('”','').replace(';','') \
        .replace('[','').replace(']','').replace('*','')


#.translate(None, string.punctuation)
#%% CLEANING
wake = wake.split(' ')[:200000]
wake.remove('')
# ORIGINAL WC: 219805

crim = crim.split(' ')[:200000]
crim.remove('')
# ORIGINAL WC: 206898

# NOW HOW THE BLOODY HELL DO WE COMPUTE THE ENTROPY ?

#%% A simple measure

def dictmaker(book):
    words = {}
    for word in book:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
    return words

wakewords = dictmaker(wake).keys()
crimwords = dictmaker(crim).keys()

print('Finnegans wake ratio of unique words to total: ' + str(len(wakewords)/200000.))
print('Crime and Punishment ratio of unique words to total: ' + str(len(crimwords)/200000.))

#%%
'''
Entropy can also be used a measure of the amount of information in system or message.
'''

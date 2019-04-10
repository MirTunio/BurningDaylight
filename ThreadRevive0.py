import random
import docx2txt
import fnmatch
import os
from datetime import datetime
import gkeepapi
import secrets1

#%% GENERATE COMPILATIOM
keep = gkeepapi.Keep()
keep.login('tuniomurtaza@gmail.com', secrets1.AP)
all_keeps = keep.all()

all_paths = []
for root, dirnames, filenames in os.walk('C:/Users/mtunio/Desktop/Writing'):
    for filename in fnmatch.filter(filenames, '*.docx'):
        all_paths.append(os.path.join(root, filename))
for root, dirnames, filenames in os.walk('C:/Users/mtunio/Desktop/NOTES'):
    for filename in fnmatch.filter(filenames, '*.docx'):
        all_paths.append(os.path.join(root, filename))
for root, dirnames, filenames in os.walk('C:/Users/mtunio/Desktop/NOTES'):
    for filename in fnmatch.filter(filenames, '*.txt'):
        all_paths.append(os.path.join(root, filename))
#all_keeps.append(all_paths)
all_comp = all_paths + all_keeps

#%% PRINTER
def fetchprint(thisone,all_comp):
    if type(thisone) == gkeepapi.node.Note or type(thisone) == gkeepapi.node.List :
        print("NOTE: " + thisone.title)
        print(thisone.timestamps.created.strftime('%Y-%m-%d'))
        print('---')
        print('')
        print(thisone.text)
    elif thisone[-4:] == '.txt':
        f = open(thisone,"r")
        TEXT = f.read()
        TITLE =  "TEXT: " + thisone.split('\\')[-1][:-4]
        print(TITLE)
        print(datetime.fromtimestamp(os.stat(thisone).st_ctime).strftime('%Y-%m-%d'))
        print('---')
        print('')
        print(TEXT)

    else:
        TITLE =  "WRIT: " + thisone.split('\\')[-1][:-5]
        print(TITLE)
        print(datetime.fromtimestamp(os.stat(thisone).st_ctime).strftime('%Y-%m-%d'))
        print('---')
        print('')

        try:
            TEXT = docx2txt.process(thisone)
            print(TEXT)
        except:
            print('Doc is empty or temp file')
            fetchprint(random.choice(all_comp),all_comp)

#%% CHOOSE ONE
choice = random.choice(all_comp)
fetchprint(choice,all_comp)

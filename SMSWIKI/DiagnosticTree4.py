"""
TUNIO 2019

Adapting SMSWIKI framework to help individuals
self diagnose

Similar target audience

Working with Ahmed Mahmood, who is designing
the diagnostic flowcharts
"""
"""
Need a radically new approach to how the tree is strtuctured and traversed
Need setflags or something else which maintains running markers which
can be used in later questions

Perhaps:
    - Ask ques in order listed on chart
    - +1 for everything moving toward a diagnosis
    - -1 for everything moving away
    - once endstate it looks at possibilities and yields most probable
    - except when a 'danger' flag is raised in which case it says go to hospital
    - ok
    
How to cycle questions:
    - same as before, but for fucks sake write the code better.
    
Record Creation:
    - run routine on every message in
    - ask if 'Ahmed' or whatever name on record, if no, create new record with same number
    - if multiple records same number, ask which patient 1 ahmed, 2 mir, etc...
    - [Fname, Lname, Age, NIC, City, Number]
"""
#%% Imports and helper functions for init
import csv
import numpy as np
from googletrans import Translator
translator = Translator() # initialzing translator 
from datetime import date

def loadtree(filename):
    with open(filename, newline='') as csvfile:
        tree_out = np.array(list(csv.reader(csvfile)))
    return tree_out

filename = 'ahmed0.csv'
diagnostic_tree = loadtree(filename)

record_name = 'record0.csv'
records = loadtree(record_name)

treatment_trees = {'AGE':'age_treatment.csv','HighFever':'highfever_treatment.csv','AGE+HighFever':'age_highfever_treatment.csv'}

def sms(text,number):
    print(qa(text,number))

#%% Session maintainance
sessions = {} # phone number:session dictionary, dict of dicts, holds all information about current session for each number
#keys: same_page:True,False (are all prelimsclear?), has_record:True/False, preferred_language:'en'/'ur'/'sd', rundex:int of where in tree, runpointers: where incoming options point, diagnostic_points:somehowwhich diagnostic points, etc...

#%% Helper functions for question cycling
def in_record(from_number):
    global records
    return from_number in records

def optChoice(fulltext):
    # SHOULD ADD TRY EXCEPT HERE
    return int(fulltext.rstrip().lstrip())

def fetch_names(from_number): #checks if number on file
    global records
    all_matches = np.where(records[:,5] == from_number)[0]
    all_fnames = records[all_matches][:,1]
    all_lnames = records[all_matches][:,2]
    all_IDs = records[all_matches][:,0]
    return [x[0]+' '+x[1] for x in zip(all_fnames,all_lnames)], all_IDs

def add_record(record_in,filename):
    global records
    newrecord = np.vstack((records,record_in))
    records = newrecord
    np.savetxt(filename, records, delimiter=",",fmt='%s') #filename
    
def endsession(from_number):
    del sessions[from_number]

def fmt(string_in):
    #translator goes here
    return string_in

def getrow(tree_in,rowdex):
    CURRENT_ROW_DEX = np.where(tree_in[:,0] == rowdex)[0][0]
    CURRENT_ROW = tree_in[CURRENT_ROW_DEX]
    return CURRENT_ROW

def is_number(text_in):
    result = False
    try:
        optChoice(text_in)
        result = True
    except:
        return False
    return result

def format_qa(q_pre,a_pre,special=''):
    a_lis = a_pre.rstrip().lstrip().replace('[','').replace(']','').split(',')
    
    if special != '':
        a_lis = special.split(',') 
        
    q_fin = q_pre+'?\n'
    
    for i in range(len(a_lis)):
        q_fin += '\n' + str(i) + ' ' + a_lis[i]
        
    q_fin = fmt(q_fin)
    return q_fin

def yield_qa(tree_in,dex,special=''):
    CURRENT_ROW = getrow(tree_in,dex)
    q_pre, a_pre = CURRENT_ROW[3].split('?')
    q_fin = format_qa(q_pre,a_pre,special=special)
    return q_fin

def getRx(dex,treatment_tree_in):
    CURRENT_ROW = getrow(treatment_tree_in,dex)
    prescription = CURRENT_ROW[3].replace('|','\n')
    return prescription
    
def nextdex(fulltext_response, prevdex, tree_in):
    choice = int(fulltext_response.lstrip().rstrip())
    oldrow = getrow(tree_in,prevdex)
    pointers = oldrow[4].split(',')
    nexdex = pointers[choice]
    flags = oldrow[5].split(',')
    
    treatment = 'treatment' in str(flags) or 'prescription' in str(flags)
    
    hypothesis = flags[choice]
    return nexdex, hypothesis, treatment
    
    
def qa(fulltext, from_number): #given list of questions, options, and where they point, select which question to pose next and read response
    global sessions
    global records
    global record_name
    
    
    # Setting up session if not already set up...
    if from_number not in sessions:
        sessions[from_number] = {}
        sessions[from_number]['same_page'] = False # Normally False, has to check all kinds of prelims and create records set name etc.
        sessions[from_number]['same_page_track'] = 0
        sessions[from_number]['treatment'] = False
        sessions[from_number]['hypothesis'] = []
        sessions[from_number]['diagnosing'] = False # Normally False, skipping same_page crap
        sessions[from_number]['diagnosing_track'] = 0
        sessions[from_number]['rundex'] = '0'
        sessions[from_number]['treatment_track'] = 0
        sessions[from_number]['treatment_for'] = ''
        sessions[from_number]['ID'] = ''
        sessions[from_number]['TEMP'] = ''
        sessions[from_number]['followup'] = False
        sessions[from_number]['followup_track'] = 0
        sessions[from_number]['Rx'] = False
        sessions[from_number]['record_creation_encours'] = False
        
        
    # SAME PAGE
    if not sessions[from_number]['same_page']: # Get on the same page, routine
        if in_record(from_number) and not len(sessions[from_number]['TEMP'])>0 and not sessions[from_number]['record_creation_encours']:
            names,IDs = fetch_names(from_number)
            who_dis = 'Is your name listed below, enter the number, if not reply "no"'
            sessions[from_number]['TEMP'] = IDs
            response = format_qa(who_dis,str(names))
            return fmt(response)
        
        elif in_record(from_number) and len(sessions[from_number]['TEMP'])>0 and not fulltext.lower().lstrip().rstrip() == "no" and not sessions[from_number]['record_creation_encours']:
            if not is_number(fulltext):
                response = 'Please reply with a number from options above'
                return fmt(response)
            elif optChoice(fulltext) not in range(len(sessions[from_number]['TEMP'])):
                response = 'Please reply with a number from options above'
                return fmt(response)
                
            sessions[from_number]['ID'] = sessions[from_number]['TEMP'][optChoice(fulltext)]
            sessions[from_number]['same_page'] = True
            sessions[from_number]['same_page_track'] += 1
            
            RECORD_IN = getrow(records,sessions[from_number]['ID'])
            sessions[from_number]['fname'] = RECORD_IN[1]
            sessions[from_number]['lname'] = RECORD_IN[2]
            sessions[from_number]['age'] = RECORD_IN[3]
            sessions[from_number]['city'] = RECORD_IN[4]
            
            if 'followup' == RECORD_IN[5]:
                sessions[from_number]['followup'] = True
            else:
                sessions[from_number]['diagnosing'] = True
                 
        else:
            sessions[from_number]['record_creation_encours'] = True
            q1 = ('fname', "Creating Record:\nWhat is patient's first name?")
            q2 = ('lname', "What is patient's last name?")
            q3 = ('age', "What is patient's age?")
            q4 = ('city', "What city is patient in?")
            RecordCreationQues = [q1,q2,q3,q4,('done','done')]

            recdex = sessions[from_number]['same_page_track']
            next_record_q = RecordCreationQues[recdex][1]
            
            if recdex == 0:
                sessions[from_number]['same_page_track'] += 1
                return fmt(next_record_q)
            elif next_record_q == 'done':
                sessions[from_number][RecordCreationQues[recdex-1][0]] = fulltext.rstrip().lstrip()
                sessions[from_number]['diagnosing'] = True
                sessions[from_number]['same_page'] = True
                sessions[from_number]['ID'] = str(int(records[-1][0])+1)
                add_record([sessions[from_number]['ID'],sessions[from_number]['fname'],sessions[from_number]['lname'],sessions[from_number]['age'],sessions[from_number]['city'],str(from_number),''],record_name)
                
                response = 'Record created, reply with "diagnose" to start diagnosis'
                return fmt(response)
            else:
                sessions[from_number][RecordCreationQues[recdex-1][0]] = fulltext.rstrip().lstrip()
                sessions[from_number]['same_page_track'] += 1
                return fmt(next_record_q)
            
            
    # FOLLOWING UP
    if sessions[from_number]['followup']:
        if sessions[from_number]['followup_track'] == 0:
            response = "Would you like to followup on your previous complaint? \n0 Yes\n1 No"
            sessions[from_number]['followup_track'] += 1
            return fmt(response)
        
        elif sessions[from_number]['followup_track'] == 1:
            if is_number(fulltext) and optChoice(fulltext) in range(2):
                choice = optChoice(fulltext)
                if choice == 0:
                    sessions[from_number]['followup_track'] += 1
                    response = 'Are you still suffering symptoms? \n0 Yes\n1 No'
                    return fmt(response)
                elif choice == 1:
                    sessions[from_number]['diagnosing'] = True         
            else:
                response = 'Please reply with a number from options above'
                return fmt(response)
            
        elif sessions[from_number]['followup_track'] == 2:
            if is_number(fulltext) and optChoice(fulltext) in range(2):
                choice = optChoice(fulltext)
                if choice == 0:
                    response = 'Please visit your nearest hospital! \nReply with the name of your city to recieve list of nearby hospitals/care centers.\nSession ended, for a second opinion reply: diagnose \n\n\n[SMSDIAGNOSISTUNIO2019]'
                    return fmt(response)
                elif choice == 1:   
                    response = 'Stop treatment and return to baseline remedies for 1 week' + '\n\nThank you for using sms-diagnosis!\nSession ended, for a second opinion reply: diagnose \n\n\n[SMSDIAGNOSISTUNIO2019]'
                    return fmt(response)
            else:
                response = 'Please reply with a number from options above'
                return fmt(response) 
            
            
    # DIAGNOSING  
    diagnostic_tree = loadtree('ahmed0.csv') # doing this for now
    if sessions[from_number]['diagnosing']: # Diagnostic routine    
        
        if fulltext.lstrip().rstrip() == 'end':
            endsession(from_number)
            response = 'Session ended by user...' + '\n\nThank you for using sms-diagnosis!\nSession ended, for a second opinion reply: diagnose \n\n\n[SMSDIAGNOSISTUNIO2019]'
            return fmt(response)
            
        if fulltext.lstrip().rstrip() == 'diagnose' and sessions[from_number]['diagnosing_track'] == 0:
            sessions[from_number]['rundex'], hypothesis, treatment = nextdex('0', sessions[from_number]['rundex'], diagnostic_tree)
        elif is_number(fulltext) and optChoice(fulltext) in range(len(getrow(diagnostic_tree,sessions[from_number]['rundex'])[4].split(','))):
            sessions[from_number]['rundex'], hypothesis, treatment = nextdex(fulltext, sessions[from_number]['rundex'], diagnostic_tree)
        elif sessions[from_number]['diagnosing_track'] > 0:
            response = 'Please reply with a number from options above'
            return fmt(response)              
            
        if fulltext.lstrip().rstrip() == 'diagnose':
            sessions[from_number]['diagnosing_track'] += 1
            
        if sessions[from_number]['diagnosing_track'] == 0:
            response = 'Please reply with "diagnose" to start diagnosis'
            return fmt(response)   
            
        if treatment:
            sessions[from_number]['treatment'] = True
            sessions[from_number]['diagnosing'] = False
            sessions[from_number]['hypothesis'].append(hypothesis)
        else:    
            sessions[from_number]['hypothesis'].append(hypothesis)
            next_question = yield_qa(diagnostic_tree,sessions[from_number]['rundex'],special='')
            return next_question
        
        
    # TREATING    
    if sessions[from_number]['treatment']:
        if sessions[from_number]['treatment_track'] == 0:
            hypothesis_in = sessions[from_number]['hypothesis']
            hypostring = str(hypothesis_in)
            
            if 'danger' in hypostring:
                sessions[from_number]['treatment_track'] += 1
                sessions[from_number]['treatment_for'] = 'DANGER'
                response = 'Patient is in a HIGH risk condition!! \nReply with the name of your city to recieve list of nearby hospitals/care centers\nSession ended, for a second opinion reply: diagnose '+ '\n\n\n[SMSDIAGNOSISTUNIO2019]'
                endsession(from_number)
                return fmt(response)
            
            elif 'AGE' in hypostring and'high grade fever' in hypostring:
                sessions[from_number]['treatment_track'] += 1
                sessions[from_number]['treatment_for'] = 'AGE+HighFever'
                sessions[from_number]['rundex'] = '0'
    
            elif 'AGE' in hypostring:
                sessions[from_number]['treatment_track'] += 1
                sessions[from_number]['treatment_for'] = 'AGE'
                sessions[from_number]['rundex'] = '0'
                
            elif 'high grade fever' in hypostring:
                sessions[from_number]['treatment_track'] += 1
                sessions[from_number]['treatment_for'] = 'HighFever'
                
            else:
                response = 'Patient is in a low risk condition. \nPlease reply with "diagnose" for a second opinion\nSession ended, for a second opinion reply: diagnose ' + '\n\n\n[SMSDIAGNOSISTUNIO2019]'
                endsession(from_number)
                return fmt(response)
        
        treatment_tree = loadtree(treatment_trees[sessions[from_number]['treatment_for']])

        sessions[from_number]['rundex'], hypothesis, stopflag = nextdex(fulltext, sessions[from_number]['rundex'], treatment_tree)
        sessions[from_number]['Rx'] = stopflag
        if not stopflag:
            next_question = yield_qa(treatment_tree, sessions[from_number]['rundex'], special='')
            return next_question
        else:
            prescription = getRx(sessions[from_number]['rundex'], treatment_tree)
            response = prescription + '\n\nThank you for using sms-diagnosis!\nSession ended, for a second opinion reply: diagnose \n\n\n[SMSDIAGNOSISTUNIO2019]'
            endsession(from_number)
            return fmt(response)

#%%
"""
AFTER: 
    > ADD DEHYDRATION QUESTIONS TO ahmed0.csv with appropriate flags etc... will need to move treatment markers to 'branch4' situation
    > Followup routine
NOTES:    
    ON RECORDS AND CREATION:
        Add previous complaints to records > endsession(), savesession parameter to add to records
    
    
"""
    
    

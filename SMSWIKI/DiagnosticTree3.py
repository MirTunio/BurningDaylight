"""
TUNIO 2019

Adapting SMSWIKI framework to help individuals
self diagnose

Similar target audience

Working with Ahmed Mahmood, who is designing
the diagnostic flowcharts
"""

"""
Overview:
> One patient file, logs all past complaints and notes from doctors etc., perhaps pictures as well
    > Name
    > Number (internal)
    > Last 4 digits of CNIC
    > Location (goth etc.)
    
> One diagnostic tree in a dataframe:
    > Need answer snappers and answer checkers and re-requesters
    > Navigate the tree
    > No need to be dense, set index 0-100 as initial quest, 100-200 peds, 200-300 adults etc etc. 

    > Diagnostic tree saved as csv
    > Each row is a question/state, col tells you where to go depending on answer recieved
    > Each row has unique identifier (index number seems reasonable right now)
"""

#%%
import pandas as pd
from googletrans import Translator
from datetime import date

#%%
#Loading Diagnostic Tree and Patient Records
#dtree = pd.read_csv("treeMir.csv", index_col=0) #Loading diagnostic tree
dtree = pd.read_csv("ahmed0.csv", index_col=0) #Loading diagnostic tree
record_name = 'smsdiagrecord'
record_holder = pd.read_pickle(record_name) #Loading patient records, all to memory for now... 


#Creating session variables, so each number has its own session on same instance
response_holder = {} # FROMNUMBER:[LIST OF RESPONSES], a record of responses in particular session
rundex_holder = {} # FROMNUMBER:rundexvalue, a variable for locating where they are in the diagnostic tree
runPointers_holder = {} # FROMNUMBER:runpointerslist, a variable for each number holding the tree location which the sms responses point to (e.g. response: 0, RunPointers[number][0] = 24 (row 24 of tree))
language = 'en' #'ur','sd' # Potential languages available, in principle all of google translate langs available. But will focus on phrasing which can be translated into these 3
translator = Translator() # initialzing translator 
createRecord_holder = [] # FROMNUMBER:Boolean, is True if creating record at the moment
ASKED_holder = {} # FROMNUMBER:[list of answers] Tracks progress in record creation subroutine
flag_holder = {} # FROMNUMBER:[list of flags] Tracks flags to be checked before diagnosis
prevdex_holder = {}
#%%
def Qprocess(q_string_in): # Parses the Diagnostic Tree and pulls out the questions and options
    qs, opts = q_string_in.split('?')
    OPTLIST = opts.lstrip().rstrip().replace('[','').replace(']','').split(',')
    QUES = qs + '?'
    return QUES, OPTLIST

def Pprocess(p_string_in): # Pulls out the pointers (to next question) from row in Diagnostic Tree
    return p_string_in.split(',')
    
def format_response(string_in): # Helper function to do final formatting and translations to output.
    global language
    global translator
    
    if language == 'en': # English
        return string_in
    elif language == 'ur': # Urdu
        return translator.translate(string_in, dest='ur', src='en').text
    elif language == 'sd': # Sindhi
        return translator.translate(string_in, dest='sd', src='en').text
    return string_in

def langchange(newlangcode): # Helper to change the language
    global language
    language = newlangcode

def getQuestion(questionID): # Takes a row ID in Diagnostic Tree and returns well formatted question.
    global dtree
    q_string = dtree.loc[questionID].question
    QUES,OPTS = Qprocess(q_string)
    fmtdq = ''
    
    fmtdq += QUES+'\n'
    for i in range(len(OPTS)):
        fmtdq += str(i) + "  " + OPTS[i]+'\n'  
    return fmtdq
    
def refresh_record(): # Resets the record on file, for testing purposes only.
    global record_name
    RECORDS = pd.DataFrame(columns=['first_name','last_name','age','cnic','location','number','previous_complaints'])
    RECORDS.to_pickle(record_name)
    load_record()
    
def save_record(): # Save the record
    global record_holder
    record_holder.to_pickle(record_name)
    
def load_record():
    global record_holder
    global record_name
    record_holder = pd.read_pickle(record_name)
    print('records loaded...')
    
def endsession(from_number): # Ends session immeadiately, clears session history for number
    if from_number not in response_holder:
        return 'no active session with {} to end...'.format(from_number)
        
    responses_this_session = response_holder[from_number] #Adding responses to records
    for i, row in record_holder.iterrows():
        if row.number == from_number:
            new_prev_comp = row.previous_complaints
            responses_this_session.insert(0,date.today().strftime("%Y.%m.%d"))
            new_prev_comp.append(responses_this_session)
            record_holder.at[i,'previous_complaints'] = new_prev_comp
    save_record()
    
    del response_holder[from_number]
    del rundex_holder[from_number]
    del runPointers_holder[from_number]    
    return 'ok'


def RecordCreator(fulltext, from_number): # ToDo: Needs work, make way to create nicely
    global record_holder
    global ASKED_holder
    
    if from_number not in ASKED_holder:
        ASKED_holder[from_number] = []
    
    q1 = "Creating Record:\nWhat is patient's first name?"
    q2 = "What is patient's last name?"
    q3 = "What is patient's age?"
    q4 = "What is patient's CNIC? (if registered)"
    q5 = "What city is patient in?"
    Q = [q1,q2,q3,q4,q5,'done']
    
    if len(ASKED_holder[from_number]) == 5:
        A = ASKED_holder[from_number]
        record_holder = record_holder.append({'first_name':A[0], 'last_name':A[1], 'age':A[2], 'cnic':A[3], 'location':A[4], 'number': from_number,'previous_complaints':[['DATE',11,33,33,77]]}, ignore_index=True)
        save_record()
        createRecord_holder.remove(from_number)
        response = 'Record created, please reply with "diagnose" to begin diagnosis'
        return format_response(response)
    elif fulltext.lstrip().rstrip() == 'new record':
        Qask = Q[len(ASKED_holder[from_number])]
        return Qask
    else:
        Qask = Q[len(ASKED_holder[from_number])+1]
        ASKED_holder[from_number].append(fulltext.lstrip().rstrip())
        if Qask == 'done':
            return RecordCreator(fulltext,from_number)
        else:
            return Qask
        
def setFlags(rundexat, from_number, choice):
    global dtree
    global flag_holder 
    
    flagsout = dtree.loc[rundexat].setflag
    
    if flagsout != 'no':
        flags = flagsout.split(',')
        flag_holder[from_number].append(flags[choice])
        

def smsqa(fulltext, from_number): # Primary message handling routine, takes text message and number from envaya_test_4/WikiHelper2 and processes result
    global record_holder
    global response_holder
    global rundex_holder
    global runPointers_holder
    global prevdex_holder
  
    #HELPER ROUTINES
    if fulltext == 'refresh record' and '3212008100' in from_number: # resets/refreshes record, for testing use.
        refresh_record()
        return 'record reset...'

    if fulltext.lstrip().rstrip() == 'new record' or from_number in createRecord_holder:
        if from_number not in createRecord_holder:
            createRecord_holder.append(from_number)
        response = RecordCreator(fulltext, from_number)
        return format_response(response)      
    
    elif from_number not in record_holder.number.values:
        response = 'No record on file, reply with "new record"'# If patient not on file, prompt to create one
        return format_response(response)
    
    if 'end' in fulltext: # ends session
        response = 'Thank you for using sms diagnosis, session ended.'
        out = endsession(from_number)
        
        if out != 'ok':
            return out
        else:
            return format_response(response)
    
    if fulltext == 'urdu': # changes language to urdu
        langchange('ur')
    elif fulltext == 'sindhi': # //
        langchange('sd')
    elif fulltext == 'english': # //
        langchange('en')
    
    
    #STARTS OFF DIAGNOSIS
    if from_number not in response_holder and 'diagnose' in fulltext: # Starts new session if number not currently in session
        flag_holder[from_number] = []
        response_holder[from_number] = [0]
        OptChoice = 99887766
    elif from_number not in response_holder and 'diagnose' not in fulltext:
        response = "Reply with 'diagnose' to begin your diagnosis"
        return format_response(response)
    else:    
        try:
            OptChoice = int(fulltext.rstrip().lstrip()) # gets choice from text of sms, catches 'not a number' errors here
        except ValueError:
            response = "Invalid response, please enter a number: {} corresponding to your answer".format(list(range(len(runPointers_holder[from_number]))))
            return format_response(response)
    
    #RUNS THROUGH THE TREE
    if OptChoice == 99887766: # Just a placegolder OptChoice for signalling start
        rundex_holder[from_number] = 0 # Start diag with first element of table
        prevdex_holder[from_number] = 0 
        first_question = getQuestion(rundex_holder[from_number]) #'This is the first question'
        response = 'Welcome to smsdiagnosis:\n\n{}'.format(first_question)
        runPointers_holder[from_number] = Pprocess(dtree.loc[rundex_holder[from_number]].pointers)
        return format_response(response)
    else:
        setFlags(prevdex_holder[from_number],from_number,OptChoice)
        response_holder[from_number].append(OptChoice)  
        
        if OptChoice not in range(len(runPointers_holder[from_number])): # catches 'number not in range of options' here
            response = "Invalid response, please enter a number: {} corresponding to your answer".format(list(range(len(runPointers_holder[from_number]))))
            return format_response(response)
        
        rundex_holder[from_number] = int(runPointers_holder[from_number][OptChoice])
        prevdex_holder[from_number] = rundex_holder[from_number]
        
        TYPE = dtree.loc[rundex_holder[from_number]].type
        
        if TYPE == 'treatment': # Checks if the session is ended and a treat, if so replies with treatment and ends the session
            if 'danger' in flag_holder[from_number]:
                response = dtree.loc[98].question
                response += '\n\nThank you for using sms diagnosis, session ended.'
                endsession(from_number)
                return format_response(response)
            
            if 'AGE' in flag_holder[from_number]:
                response = dtree.loc[97].question
                response += '\n\nThank you for using sms diagnosis, session ended.'
                endsession(from_number)
                return format_response(response)
            
            response = 'TREATMENT:\n' + dtree.loc[rundex_holder[from_number]].question
            response += '\n\nThank you for using sms diagnosis, session ended.'
    
            endsession(from_number)
            return format_response(response)
        
        next_question = getQuestion(rundex_holder[from_number]) # gets next question to send, properly formatted
        response = next_question # the text of the next question
        runPointers_holder[from_number] = Pprocess(dtree.loc[rundex_holder[from_number]].pointers) # sets pointers for the replies
        return format_response(response)

    
#%% Notes:
"""
1. Start converting Ahmed's Tree
2. Implement answer snappers if needed
3. Fix urdu translations (make catches for '' signs)
3. Find speedups, optimize
 

hint: Need all kinds of catches here (go through code again)

NOTES:
    Need to add risk factor functionality (which can be checked later to modify questions)
    risk factors include high grade fever, new symptoms etc.
    
    If AGE* on one branch and No on other it drops out
    It should ideally point to diagnosis of AGE or probably AGE but still complete diagnosis
    
    Go through all questions and set flags
    Once hit endstate, look at flags to check diagnosis
"""
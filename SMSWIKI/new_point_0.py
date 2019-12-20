"""
TUNIO 2019
tuniomurtaza@gmail.com

Python Envaya Wiki Client 
NOW WITH THE SESSIONS FOR EACH NUMBER IT SHOULD HAVE HAD...

[Explore https://smsgateway.me/ in future ...]

latest - 19/12/2019
"""

from flask import Flask, request, jsonify
import Wikihelper2
import time
import json

app = Flask(__name__)

@app.route('/echo', methods=['GET', 'POST', 'OPTIONS'])
def echo():
    """ takes the message forwarded by the envaya client on the phone and sends
    it back to the sender, exactly. Used for testing..."""
    form_in = request.form
    ACTION_IN = form_in['action']
    print("ACTION IN: " + form_in['action'])
    print("")
    
    if ACTION_IN == 'incoming':
        FROM = form_in['from']
        MSG = form_in['message']
        print("recieved message from {}:".format(FROM)) 
        print(MSG)
        print("replying with:")
        sending = jsonify({'events':[{'event': 'send', 'messages':[{'id':'123123','to':FROM,'message': MSG}]}]})
        print(sending.get_data())
        print("")
        return sending
    
    elif ACTION_IN == 'send_status':
        print('recieved STATUS: ' + form_in['log'])
        return jsonify({'events':''} )

		
def get_wiki(body, from_number): #helper function to pass message to Wikihelper and catch unexpected errors so they	aren't passed to users
    try:
        return Wikihelper2.wiki(body, from_number)    
    except:
        return "An error occured, please try something different!"
    
	
@app.route('/sms', methods=['GET', 'POST', 'OPTIONS'])
def wiki():
    """ this function takes the incoming message, sends the body of the message
    to the Wikihelper module, and sends the result back to the Envaya app using
    the appropriate formatting"""
    
    form_in = request.form
    ACTION_IN = form_in['action']
    print("\n"+"*****")
    print("ACTION IN: " + form_in['action'] + "\n")
    
    if ACTION_IN == 'incoming':
        FROM = form_in['from']
        MSG = form_in['message']
        print("Recieved message from {}:".format(str(FROM)))
        print('"'+MSG+'"')
        reply = get_wiki(MSG,FROM) # Passes message to Wikihelper and stores response in 'reply'
        sending = jsonify({'events':[{'event': 'send', 'messages':[{'id':FROM+'::'+str(time.time()),'to':FROM,'message': reply}]}]})
        print("\nReplying with:")
        print('"'+reply+'"'+"\n")
        return sending
    
    elif ACTION_IN == 'send_status':
        print('LOG: ' + form_in['log'])
        #print('FULL STATUS: ')
        #print(json.dumps(form_in, indent=4))
        print("")
        return jsonify({'events':''} ) # Properly formatted response with no content, just so envaya app doesn't freak out.

if __name__ == "__main__":
    app.run(debug=True) #TODO: Needs to be replaced with WSGI server	or something. Local usage only tho so chill. Just dk how it handles multiple requests, need to test with friends. 
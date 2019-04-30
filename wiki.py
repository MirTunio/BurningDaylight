"""
TUNIO 2019
Creating an sms based wikipedia portal 
Future: Convert to urdu (witness the fitness)
    
FIRST: Sessionless paradigm
SECND: Session paradigm with 'reply 1 for xyz' schema
    > Will need session logs
    > Session logs should store wikipediq query
    
CONSIDER: That you can run this on your own phone, no Twilio intermediary... 
    > Search for python messasge responder or something. 
"""

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import Wikihelper 

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])

def incoming_sms():
    body = request.values.get('Body', None)
    from_number = request.values.get('From')  
    resp = MessagingResponse()  
    
    response_string = Wikihelper.wiki(body)
    
    formatted_response = str(resp.message(response_string))
    return formatted_response


if __name__ == "__main__":
    app.run(debug=True)


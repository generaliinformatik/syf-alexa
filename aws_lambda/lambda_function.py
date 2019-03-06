from __future__ import print_function
import PySigfox as SF
from datetime import datetime
import os

# We'll start with a couple of globals...
CardTitlePrefix=os.environ['Card_Title_Prefix']
syfconfig_appname=os.environ['Skill_Name']
syfconfig_device = os.environ['Sigfox_Device_ID']
syfconfig_sigfoxusername=os.environ['Sigfox_API_Username']
syfconfig_sigfoxpassword=os.environ['Sigfox_API_Password']
syconfig_offset_hour=+1

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Build a speechlet JSON representation of the title, output text, 
    reprompt text & end of session
    """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': CardTitlePrefix + " - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """
    Build the full response JSON from the speechlet response
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Willkommen bei " + syfconfig_appname
    speech_output = "Willkommen bei " + syfconfig_appname + ". " + say_temperatur(os.environ['Skill_Answer_DefaultMode'],0) + " Wuenschen Sie weitere Informationen?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Es tut mir leid - ich habe Sie nicht verstanden. Wie darf ich Ihnen helfen?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Sitzung beendet"
    speech_output = "Bis bald! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def say_temperatur(level="standard", speech_output=0):
    """
    Return a suitable greeting...
    """
    card_title = "Status des Geraets ('"+syfconfig_device+"')"
    
    myListDegree = []  
    myListTime = [] 
     
    s = SF.PySigfox(syfconfig_sigfoxusername, syfconfig_sigfoxpassword)
    messages = s.device_messages(syfconfig_device)
    for msg in messages:
    	if len(msg['data']) == 4:
    		version = int(msg['data'][:2],16)
    		temp_dec = ((int(msg['data'][2:],16)-80)/2)
    		myListDegree.append(temp_dec)
    		myListTime.append(msg['time'])
    
    temp_now=myListDegree[0]
    temp_beforenow=myListDegree[1]
    temp_diffnow=(temp_now-temp_beforenow)
    if temp_diffnow == 1:
    	temp_difftext="Dies ist " + str(abs(temp_diffnow)) +" Grad mehr als die vorherige Messung. "
    elif temp_diffnow > 1:
    	temp_difftext="Dies sind " + str(abs(temp_diffnow)) +" Grad mehr als die vorherige Messung. "
    elif temp_diffnow == -1:
    	temp_difftext="Dies ist " + str(abs(temp_diffnow)) +" Grad weniger als die vorherige Messung. "
    elif temp_diffnow < -1:
    	temp_difftext="Dies sind " + str(abs(temp_diffnow)) +" Grad weniger als die vorherige Messung. "
    elif temp_diffnow == 0:
    	temp_difftext="Dieser Wert entspricht der vorherigen Messung. "
    else:
        temp_difftext="Es wurde ein Problem festgestellt."
    
    months = ["Unbekannt",
    		  "Januar",
    		  "Februar",
    		  "Maerz",
    		  "April",
    		  "Mai",
    		  "Juni",
    		  "Juli",
    		  "August",
    		  "September",
    		  "Oktober",
    		  "November",
    		  "Dezember"]
    
    myListTime[0]=myListTime[0]+(int(syconfig_offset_hour)*60*60)
    temp_day=datetime.utcfromtimestamp(myListTime[0]).day
    temp_month=months[datetime.utcfromtimestamp(myListTime[0]).month]
    temp_year=datetime.utcfromtimestamp(myListTime[0]).year
    temp_count=(len(myListDegree))
    temp_average=int(round(sum(myListDegree) / len(myListDegree)))
    temp_max=int(round(max(myListDegree)))
    temp_min=int(round(min(myListDegree)))
    temp_date=str(temp_day) +". " + str(temp_month) + " " + str(temp_year)
    temp_time=datetime.utcfromtimestamp(myListTime[0]).strftime('%H:%M:%S')
    greeting_string = "Der Sensor in der Kueche misst zuletzt " + str(temp_now) + " Grad. "

    if level == "short":
        greeting_string = str(temp_now) + " Grad. "
    if level == "details":
        greeting_string = greeting_string + temp_difftext + " Die Durchschnittstemperatur betraegt " + str(temp_average) + ", die niedrigste gemessene Temperatur betraegt " + str(temp_min) + "  und die hoechste " + str(temp_max) + " Grad. Die letzte Messung erfolgte am " + temp_date + " um " + temp_time +"."
    if speech_output == 1:
        return build_response({}, build_speechlet_response(card_title, greeting_string, "Ask me to say hello...", True))
    else:
        return greeting_string

def say_team():
    """
    Return a suitable greeting...
    """
    card_title = "Team"
    greeting_string = "Das Team " + syfconfig_appname + " besteht aus Martina, Jeanette, Max, Stephan und Rene. Wir haben die Loesung im Rahmen des Hackathon 2018 konzipiert und umgesetzt. Wir bedanken uns bei allen Unterstuetzern."
    return build_response({}, build_speechlet_response(card_title, greeting_string, "Ask me to say hello...", True))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "short":
        return say_temperatur("short",1)
    elif intent_name == "details":
        return say_temperatur("details",1)
    elif intent_name == "team":
        return say_team()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
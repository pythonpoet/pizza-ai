#!/usr/bin/python
from flask import Flask, request, jsonify,redirect,g,request,redirect,Response
import time
from flask_svelte import render_template
import datetime
from threading import Thread
from .chaosChain import *
import json
base_url='http://100.101.54.114:11434'

#from __main__ import app #, chaosLLM, user_id,user_name, session_id,t
from app import app, llm

list_of_strings = [
    "A dish with my leftovers",
    "Meal prepared in a mikrowave",
    "A meal with only red ingredience",
    "Meal prepared in a dishwasher",
    "A meal that accounts for my alegies",
    "Only fresh products"
    ]

# networkx
# altair
# gaphi graphs
class Session:
    session_id=None
    messages=[]
    message_request=None
    users=[]
    root_user=None
    stream_init=True

    def __init__(self,session_id, ):#user_id):
        self.session_id = session_id
        self.llm = ChaosLLM()
    #    self.subscribe_user(user_id)
    def subscribe_user(self,user_id):
        if not user_id in self.users:
            self.users.append(user_id)
    def init_stream(self, message):
        # multiuser addon
        self.stream_init = True
        self.messages.append(
            {
            'role': 'user',
            'content': message,
            },
        )
    def stream(self):
        if self.stream_init:
            self.stream_init = False
            response=''
            for chunk in self.llm.stream(messages=self.messages):
                response += chunk['message']['content']
                yield f"data: {json.dumps(chunk)}\n\n"
            self.messages.append(
            {
            'role': 'assistant',
            'content': response,
            },
        )

sessions={}


message_content=''
messages = []   



@app.route('/')
def index():
    global sessions
    import random
    session_id = str(random.randint(1000, 9999))
    sessions[session_id] = Session(session_id=session_id)
    return redirect(f'/{session_id}')

#@t.include
@app.route('/<string:session_id>')
def session(session_id):
    global sessions

    if not session_id in sessions.keys():
        sessions[session_id] = Session(session_id=session_id)
        print("chaos_llm messages: ", sessions[session_id].llm.messages)
        print("session_messages: ",sessions[session_id].messages )
    
    # TODO add user to session here
    
    return render_template('index.html', session_id=session_id)


@app.route('/send_message', methods=['POST'])
def send_message():
    global message_content,sessions
    data = request.json
    message_content = data['message']
    session_id = data['session_id']
    print(f'session_id:{session_id}, sessions: {sessions.keys()}')
        # Check if session_id exists in session dictionary
    if session_id in sessions.keys():
        sessions[session_id].init_stream(message_content)
        # also a stream_id could be generated here that the javascript then subscribes.
        return session_id, 200
    else:
        raise Exception(f"Session, session_id:{session_id} not found")
        return 'session not found', 404
    

@app.route('/get_message', methods=['GET'])
def get_message():
    global message_content
    print(f'prompt: {message_content}')
    return "None"
"""     response = llm.chat(messages=[{
            'role': 'user',
            'content': message_content,
            }])
    return jsonify(response) """

@app.route('/stream_message/<string:session_id>')
def stream_message(session_id):
    return Response(sessions[session_id].stream(), content_type='text/event-stream') , 200



@app.route('/get_messages')
def get_messages():
    return {'messages': messages}

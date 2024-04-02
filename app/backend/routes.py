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
from app import app
#app = Flask(__name__)



#app = Flask(__name__, template_folder='templates', static_folder='static')
#chaosLLM = ChaosLLM()
list_of_strings = [
    "A dish with my leftovers",
    "Meal prepared in a mikrowave",
    "A meal with only red ingredience",
    "Meal prepared in a dishwasher",
    "A meal that accounts for my alegies",
    "Only fresh products"
    ]

user_in_session = [
    {
        'user_ID': '',
        'user_Name': ''
    }
]

message_format = [
    {
        'timestamp_sent': '', # time of message message 
        'role': '', # 'user', 'assistant', 
        'name': '', # username
        'display_message':'', # text displayed
        'content':'' # text to llm

    }
]


messages = []   
def llm_response(msg, llm):
    stream = llm.invoke(msg['content'])
    
    # The response is being assigned before the whole stream arrives
    # A dict is an mutable object so i can just update a part of it whithout having to reassign or iterate 
    # the whole object. This is what makes it look like the text is life generatet on the website
    message = {'sent_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'sender': 'llm', 'content': '' }
    messages.append(message)
    for chunk in stream:
        message['content'] += chunk['message']['content']
    

@app.route('/')
def index():
    global session_id
    import random
    session_id = random.randint(1000, 9999)
    return redirect(f'/{session_id}')

#@t.include
@app.route('/<int:init_session_id>')
def session(init_session_id):
    global session_id
    session_id = init_session_id
    #g.track_var["session_id"] = session_id
    return render_template('index.html', session_id=session_id)


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message_content = data['message']
    print(f'from python: {message_content}')
    return 'message recived', 200

@app.route('/events')
def events():
    def generate():
        # This is a mock generator function.
        # In a real-world scenario, you would replace this with
        # your logic to generate the SSE messages.
        for i in range(10):
            yield f"data: Message from david {i}\n\n"
            time.sleep(1)  # Simulate delay between messages

    return Response(generate(), content_type='text/event-stream')

""" @app.route('/')
def index():
    global session_id
    import random
    session_id = random.randint(1000, 9999)
    return redirect(f'/{session_id}')

#@t.include
@app.route('/<int:init_session_id>')
def session(init_session_id):
    global session_id
    session_id = init_session_id
    #g.track_var["session_id"] = session_id
    return render_template('index.html', session_id=session_id) """

@app.route('/get_ideas', methods=['GET'])
def get_ideas():
    return jsonify(list_of_strings)


""" @app.route('/send_message', methods=['POST'])
def send_message():
    message_content = request.form['message']
    sender = 'You'
    sent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = {'sent_time': sent_time, 'sender': sender, 'content': message_content}
    messages.append(message)

    
    Thread(target=llm_response, args=(message,chaosLLM)).start()
    return '', 204 """

@app.route('/get_messages')
def get_messages():
    return {'messages': messages}

if __name__ == '__main__':
    app.run(debug=True)



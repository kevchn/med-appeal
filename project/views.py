#!/usr/bin/python

import json
import os, glob
import time
from datetime import date
from flask import Flask, Response, request, render_template
from project import app

result_string = ""
reset = True
count = 0
reason = ""

questions_basic = [ # 9 questions, 0-8 indices
"What's your name?", # 0
"And what's your address?", # 1
"What's your phone number?", # 2
"What's your physician's name?", # 3
"What's the address of your doctor/physician's office?", # 4
"What's your claim number?", # 5
"What's the name of your insurance provider?", # 6
"What's your policy number?", # 7
"What illness are you seeking treatment for?", # 8
"Why was your procedure denied?" #9
]
answers_basic = []

questions_lack_of_payment = [
"What are your reasons for neglecting your payments?"  # bulleted form
]
answers_lack_of_payment = []

questions_unnecessary = [
"Do you have a doctor’s recommendation for this treatment?",
"Why did your doctor deem the treatment necessary?"
]
answers_unnecessary = []

questions_out_of_network = [
"What type of treatment?",  # if user says “surgery”, mention “least invasive” in the “[and least invasive option]”
"Who is the desired specialist/doctor you would like to see?", # location
"Why do you need an out of network doctor?",
"Did you visit a local specialist or doctor?" # why not enough
]
answers_out_of_network = []

questions_in_home = [
"What are the details of your in-home care plan?"  # dots into paragraphs? dont do until UX
]
answers_in_home = []

questions_experimental = [
"Is the experimental treatment safer than non-experimental treatment?",
"Has the experimental treatment been authorized for previous treatments?", # if yes, then then add to letter. otherwise, don’t mention.
"Is the experimental treatment the only treatment available?",
]
answers_experimental = []

questions_generic = [
"What procedure were you denied?",
"Why do you believe you were denied your insurance claim?",
]
answers_generic = []

@app.route('/')
@app.route('/home')
def index():
    with open('comments.json', 'w+') as f:
        f.write('[{\
                "text": "Welcome to MedAppeal, the machine-learning AI that helps you write medical insurance appeal letters quickly and simply!",\
                "type": "question"\
            }]')

    return render_template('index.html')

@app.route('/messages', methods=['GET','POST'])
def message():
    global reset
    global count
    global result_string
    global reason
    global questions_basic, answers_basic, questions_lack_of_payment, \
    answers_lack_of_payment, questions_unnecessary, answers_unnecessary, \
    questions_out_of_network, answers_out_of_network, questions_in_home, \
    answers_in_home, questions_experimental, answers_experimental, \
    questions_generic, answers_generic

    with open('comments.json', 'r') as f:
        history = json.loads(f.read())

    if request.method == 'POST':  # on submit

        new_answer = request.form.to_dict()

        if(count < 10):
            answers_basic.append(new_answer['text'])
            history.append(new_answer)
            new_question = {'id': str(int(time.time() * 1000)), 'text': questions_basic[count], 'type': "question"}
            history.append(new_question)


        if(count == 0):
            del answers_basic[0]

        if(count == 10):
            reason = new_answer['text']
            history.append(new_answer)

        today = date.today().isoformat()

        if(count >= 10):
            if "payment" in reason:
                if(count == 10):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_lack_of_payment[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count < 11):
                    answers_lack_of_payment.append(new_answer['text'])
                    history.append(new_answer)
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_lack_of_payment[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count == 11):
                    answers_lack_of_payment.append(new_answer['text'])
                    history.append(new_answer)
                    result_string = today + "<p> \
" + answers_basic[0] + "<br> \
" + answers_basic[1] + "<br> \
" + answers_basic[6] + "<br> \
" + answers_basic[7] + "<br><br>\
Dear " + answers_basic[3] + ",<br> <br>\
Please accept this letter as my appeal to " + answers_basic[6] + "'s decision to deny coverage, because " + answers_lack_of_payment[0] + ". The reason for the denial was due to lack of payments.  <br> \
 <br> \
While I understand your requirement that coverage is contingent upon timely payment of premiums, I ask that you grant an exception in this case. Should you require additional information, please do not hesitate to contact me at " + answers_basic[2] + ". I look forward to hearing from you in the near future. <br> <br> \
Sincerely, <br> \
" + answers_basic[0] + " <br> \
" + answers_basic[2] + "</p>"
                    history.append({
                    "text": "[Click here for your automatically generated report!](/results)",
                    "type": "question"
                })
            elif "unnecessary" in reason:
                if(count == 10):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_unnecessary[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count < 12):
                    answers_unnecessary.append(new_answer['text'])
                    history.append(new_answer)
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_unnecessary[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count == 12):
                    answers_unnecessary.append(new_answer['text'])
            elif "network" in reason:  # outside network covered by doctors
                if(count == 10):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_out_of_network[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count < 14):
                    answers_out_of_network.append(new_answer['text'])
                    history.append(new_answer)
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_out_of_network[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count == 14):
                    answers_out_of_network.append(new_answer['text'])
            elif "in home" in reason or "nursing" in reason:  #
                if(count == 10):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_in_home[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count < 11):
                    answers_in_home.append(new_answer['text'])
                    history.append(new_answer)
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_in_home[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count == 11):
                    answers_in_home.append(new_answer['text'])
            elif "experimental" in reason:
                if(count == 10):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_experimental[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count < 13):
                    answers_experimental.append(new_answer['text'])
                    history.append(new_answer)
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_experimental[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count == 13):
                    answers_experimental.append(new_answer['text'])
                    history.append(new_answer)
                    result_string = today + "<p> \
" + answers_basic[0] + "<br> \
" + answers_basic[1] + "<br> \
" + answers_basic[6] + "<br> \
" + answers_basic[7] + "<br> <br>\
To whom it may concern, <br> <br>\
Please accept this letter as my appeal to " + answers_basic[6] + "'s decision to deny coverage for experimental treatment. The reason for the denial was due to the request of a new experimental treatment. Appealing this decision is a right guaranteed by the Patient Self-Determination Act.<br> \
 <br> \
Upon receiving the explanation of benefits statement, I was notified by "+answers_basic[6] +" that the plan was denied it because proposed treatment was experimental. However,  my doctor, " +answers_basic[3]+ ", assured me that it was a safer/less expensive treatment. <br> \
Please review this appeal and let me know if you need anything else to consider this request. I look forward to hearing from you directly as soon as possible. <br><br> \
Sincerely, <br> " \
+ answers_basic[0] + " <br> \
" + answers_basic[2] + "</p>"
                    history.append({
                    "text": "[Click here for your automatically generated report!](/results)",
                    "type": "question"
                })
            else: # general case
                if(count == 10):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_generic[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count < 12):
                    answers_generic.append(new_answer['text'])
                    history.append(new_answer)
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_generic[count-10], 'type': "question"}
                    history.append(new_question)
                elif(count == 12):
                    answers_generic.append(new_answer['text'])
                    history.append(new_answer)
                    result_string = today + "<p> \
" + answers_basic[0] + "<br> \
" + answers_basic[1] + "<br> \
" + answers_basic[6] + "<br> \
" + answers_basic[7] + "<br><br> \
Dear " + answers_basic[6] + ",<br><br> \
Please accept this letter as my appeal to " + answers_basic[6] + "'s' decision to deny coverage for " + answers_generic[0] + ". It is my understanding that this procedure has been denied because: <br> \
" +  answers_generic[1] + " <br> \
As you know, I have been diagnosed with " + answers_basic[8] + ". Currently " + answers_basic[3] + " believes that I will significantly benefit from undergoing " + answers_generic[0] +". Please see the enclosed letter from " + answers_basic[3] + " for more details. <br> \
Based on this information, I'm asking that you reconsider your previous decision and allow coverage for the desired " + answers_generic[0] + ". [The treatment is scheduled to begin on " + today + ".] Should you require additional information, please do not hesitate to contact me at " + answers_basic[2] + ".\nI look forward to hearing from you in the near future. <br><br> \
Sincerely, <br> \
" + answers_basic[0] + " <br> \
" + answers_basic[2] + "</p>"
                    history.append({
                    "text": "[Click here for your automatically generated report!](/results)",
                    "type": "question"
                })

        count += 1

        with open('comments.json', 'w') as f:
            f.write(json.dumps(history, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps(history),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route('/results')
def res():
    return render_template('results.html', results = result_string)

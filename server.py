
# This file provided by Facebook is for non-commercial testing and evaluation
# purposes only. Facebook reserves all rights not expressly granted.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
import time
from datetime import date
from flask import Flask, Response, request, render_template

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

reset = True
count = -1
questions_basic = [
"Hi, what's your name?",
"And what's your address?",
"What's your phone number?",
"What's your physician's name?",
"What's the address of your doctor/physician's office?",
"What's your claim number?",
"What's the name of your insurance provider?",
"What's your policy number?",
"What illness are you seeking treatment for?",
]
answers_basic = []

questions_lack_of_payment = [
"What are your reasons for neglecting your payments?"  # bulleted form
]
answers_lack_of_payment = []

questions_unnecessary = [
"Do you have a doctor’s recommendation for this treatment?",
"Why did your doctor deem the treatment necessary?",
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

reason = ""

@app.route('/api/comments', methods=['GET', 'POST'])
def comments_handler():

    global reset
    global count
    global questions_basic, answers_basic, questions_lack_of_payment, \
    answers_lack_of_payment, questions_unnecessary, answers_unnecessary, \
    questions_out_of_network, answers_out_of_network, questions_in_home, \
    answers_in_home, questions_experimental, answers_experimental

    if(reset):
        one_off_time = str(int(time.time() * 1000))

        with open('comments.json', 'w') as f:
            f.write('[]')
            reset = False

    with open('comments.json', 'r') as f:
        history = json.loads(f.read())

    if request.method == 'POST':  # on submit
        reason = ""
        new_answer = request.form.to_dict()
        new_answer['type'] = "answer"
        history.append(new_answer)

        count += 1

        if(count < 9):
            new_question = {'id': str(int(time.time() * 1000)), 'text': questions_basic[count], 'type': "question"}
            history.append(new_question)
            answers_basic.append(new_answer['text'])
            print("\n\n\n" + str(count) + "\n" + str(len(answers_basic)) + "\n\n")

        if(count == 9):
            reason = new_answer['text']

        result_string = ""
        today = date.today().isoformat()

        if(count >= 9):
            # define the function blocks
            if "payment" in reason:
                if(count < 12):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_lack_of_payment[count-9], 'type': "question"}
                    history.append(new_question)
                    answers_lack_of_payment.append(new_answer['text'])
            elif "unnecessary" in reason:
                if(count < 15):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_unnecessary[count-9], 'type': "question"}
                    history.append(new_question)
                    answers_unnecessary.append(new_answer['text'])
            elif "network" in reason:  # outside network covered by doctors
                if(count < 13):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_out_of_network[count-9], 'type': "question"}
                    history.append(new_question)
                    answers_out_of_network.append(new_answer['text'])
            elif "in home" in reason or "nursing" in reason:  #
                if(count < 14):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_in_home[count-9], 'type': "question"}
                    history.append(new_question)
                    answers_in_home.append(new_answer['text'])
            elif "experimental" in reason:
                if(count < 12):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_experimental[count-9], 'type': "question"}
                    history.append(new_question)
                    answers_experimental.append(new_answer['text'])
            else:
                if(count < 12):
                    new_question = {'id': str(int(time.time() * 1000)), 'text': questions_experimental[count-9], 'type': "question"}
                    history.append(new_question)
                    answers_generic.append(new_answer['text'])
                result_string = today + " \
" + answers_basic[0] + " \
" + answers_basic[1] + " \
" + answers_basic[6] + " \
" + answers_basic[7] + " \
Dear " + answers_basic[3] + ", \
Please accept this letter as my appeal to " + answers_basic[6] + "'s' decision to deny coverage for " + answers_basic[8] + ". It is my understanding based that this procedure has been denied because: \
" + answers_generic[1] + " \
As you know, I have been diagnosed with " + answers_basic[0] + ". Currently " + answers_basic[3] + " believes that I will significantly benefit from " + answers_generic[0] +". Please see the enclosed letter from " + answers_basic[3] + " for more detail.]. \
Based on this information, I asking that you reconsider your previous decision and allow coverage for the desired " + answers_generic[0] + ". [The treatment is scheduled to begin on " + today + ".] Should you require additional information, please do not hesitate to contact me at " + answers_basic[2] + ".  I look forward to hearing from you in the near future. \
Sincerely, \
" + answers_basic[0] + " \
" + answers_basic[2] + "."
                return render_template('results.html', result_string)

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


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), debug=True)

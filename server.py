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
from flask import Flask, Response, request

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

reset = True
count = 0
questions_basic = [
"Hi, what's your name?",
# automatically generate date
"What's your phone number?",
"What's your physician's name?",
"What's the address of your doctor/physician's office?",
"What's your claim number?",
"What's a name of a contact at your insurance company?",
"What's the name of your insurance provider?",
"What's your policy number?",
"What ailment are you seeking treatment for?",
""
]
answers_basic = []
questions_lack_of_payment = []
answers_lack_of_payment = []
questions_unnecessary = []
answers_unnecessary = []
questions_out_of_network = []
answers_out_of_network = []
questions_in_home = []
answers_in_home = []
questions_experimental = []
answers_experimental = []
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
            f.write('[\n \
{ "id": "' + one_off_time + '",\n \
    "type": "question",\n \
    "text": "Hi, what\'s your name?"\n \
}\n \
]')
            reset = False

    with open('comments.json', 'r') as f:
        history = json.loads(f.read())

    if request.method == 'POST':  # on submit
        new_answer = request.form.to_dict()
        new_answer['type'] = "answer"
        history.append(new_answer)

        count += 1

        if(count < 9):
            new_question = {'id': str(int(time.time() * 1000)), 'text': questions_basic[count], 'type': "question"}
            history.append(new_question)
            answers_basic.append(new_answer)

        if(count == 9):
            reason = new_answer

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

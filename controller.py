from model import InputForm
from flask import Flask, render_template, request, Response
from compute import generate_hello
import csv, io, os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = generate_hello()
        return render_template('results.html')
    else:
        return render_template('view.html', form=form)

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)

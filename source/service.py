from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    text = ['dkoidke', 'ddkeod', 'dedpel']

    return render('templates/base', text=text)
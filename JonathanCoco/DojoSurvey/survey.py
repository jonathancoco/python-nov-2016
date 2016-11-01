from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/users', methods=['POST'])
def create_users():

    vName = request.form['name']
    vEmail = request.form['email']
    vLanguage = request.form['language']
    vLocation = request.form['location']
    vComment = request.form['comment']

    return render_template("survey_results.html", name=vName, email=vEmail, language=vLanguage, location=vLocation, comment=vComment)

@app.route('/GoBack', methods=['POST'])
def go_back():

    return redirect('/')



app.run(debug=True)

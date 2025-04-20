from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from flask import redirect, url_for
app = Flask(__name__, static_folder="static")



# ROUTES

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/piano_basics')
def piano_basics():
    return render_template("piano_basics.html")

@app.route('/song_list')
def song_list():
    return render_template("song_list.html")

@app.route('/practice')
def practice():
    return render_template("practice.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")


# AJAX FUNCTIONS




if __name__ == '__main__':
   app.run(debug = True, port=5001)





from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from flask import redirect, url_for
app = Flask(__name__, static_folder="static")

quiz_questions = [
    {"image": "missing_note_1.png", "answer": "F"},
    {"image": "missing_note_2.png", "answer": "C"},
    {"image": "type_note_1.png", "answer": "half note"},
    {"image": "type_note_2.png", "answer": "quarter note"},
]

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

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    index = int(request.args.get("q", 0))  # default to 0 if missing
    index = index % len(quiz_questions)  # wrap around
    question = quiz_questions[index]
    return render_template("quiz.html", question=question, index=index, total=len(quiz_questions))



# AJAX FUNCTIONS




if __name__ == '__main__':
   app.run(debug = True, port=5001)





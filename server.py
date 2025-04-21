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

song_list = {
    "1": {
        "title": "Mary Had a Little Lamb",
        "image": "images/mary_lamb.png",
        "measures": [
            "images/mary_measures_1.png",
            "images/mary_measures_2.png",
            "images/mary_measures_3.png",
            "images/mary_measures_4.png"
        ]
    },
    "2": {
        "title": "Happy Birthday",
        "image": "images/happy_birthday.png",
        "measures": [
            "images/happy_measures_1.png",
            "images/happy_measures_2.png",
            "images/happy_measures_3.png"
        ],
        "description": "It’s a great piece to learn for beginners. Fun fact: This is also the tune of Twinkle Twinkle Little Star",
        "song_notes": "The primary notes in this song are E, D, C, G",
    }
}

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

# have argument
@app.route('/learn_song')
def learn_song():
    song_param = request.args.get("song")

    song_title = {
        "mary_lamb": "Mary Had a Little Lamb",
        "happy_birthday": "Happy Birthday"
    }.get(song_param)

    return render_template("learn_song.html", song_title=song_title)


@app.route('/practice')
def practice():
    song_param = request.args.get("song")

    song_title = {
        "happy_birthday": "Happy Birthday",
        "mary_lamb": "Mary Had a Little Lamb"
    }.get(song_param, None)

    return render_template("practice.html", song_title=song_title)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    index = int(request.args.get("q", 0))  # default to 0 if missing
    index = index % len(quiz_questions)  # wrap around
    question = quiz_questions[index]
    return render_template("quiz.html", question=question, index=index, total=len(quiz_questions))



# AJAX FUNCTIONS




if __name__ == '__main__':
   app.run(debug = True, port=5001)





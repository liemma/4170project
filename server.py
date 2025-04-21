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

songs = {
    "1": {
        "title": "Mary Had a Little Lamb",
        "image": "images/mary_lamb.png",
        "measures": [
            "images/mary_measures_1.png",
            "images/mary_measures_2.png",
            "images/mary_measures_3.png",
            "images/mary_measures_4.png"
        ], 
        "description": "This beginner-friendly piece uses notes like E, D, C, and G to create a gentle and memorable melody. Fun fact: it shares its tune with Twinkle Twinkle Little Star, making it a great way to learn familiar patterns early on.",
    },
    "2": {
        "title": "Happy Birthday",
        "image": "images/happy_birthday.png",
        "measures": [
            "images/happy_measures_1.png",
            "images/happy_measures_2.png",
            "images/happy_measures_3.png"
        ],
        "description": "This cheerful tune is built on simple notes like G, A, C, B, D, and F. It’s a great piece for beginners to practice smooth transitions between intervals—and perfect for birthday celebrations!",
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
    song_id = request.args.get("song")
    song = songs.get(song_id)

    if not song:
        return render_template("learn_song.html", song_title=None)

    return render_template(
        "learn_song.html",
        song_title=song["title"],
        song_image=song["image"],
        song_description=song["description"],
        song_param=song_id
    )

@app.route("/learn_song_step")
def learn_song_step():
    song_id = request.args.get("song")
    step = int(request.args.get("step", 1))

    # TODO: load song data and measures
    return f"You are viewing step {step} of song {song_id}"


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





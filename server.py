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
            "images/happy_measure_1.png",
            "images/happy_measures_2.png",
            "images/happy_measures_3.png"
        ],
        "description": "This cheerful tune is built on simple notes like G, A, C, B, D, and F. It’s a great piece for beginners to practice smooth transitions between intervals—and perfect for birthday celebrations!",
    }
}

basics = {
    "1": {
        "id": "1",
        "title": "Learn the Notes",
        "image": "",
        "text": "Pianos are made up of scales, which come in sets of CDEFGAB. \n The black keys are sharps or flats, which are a half-step higher or lower than the white keys. \n The white keys are labeled with the notes below.",
        "next_lesson": "2"
    },
    "2": {
        "id": "2",
        "title": "Sheet Music",
        "image": "images/sheet_music.png",
        "text": "Sheet music is a written form of music that tells you:\n🎵 What notes to play (like C, D, E… placed on a staff of lines)\n⏱️ How long to play them (whole notes, half notes, quarter notes, etc.)\n🎹 How fast to play (called the tempo)",
        "next_lesson": "quiz"
    },
    "3":{
        "id": "3",
        "title": "How to Play",
        "image": "",
        "text": "We turned your computer keyboard into a piano keyboard! Your keys in the number row of your keyboard will control the piano keys labeled below. Try it now!",
        "next_lesson": "song_list"
    }
}

lessons = {
    "1": {
        "id": "1",
        "title": "Happy Birthday (first measures 1 & 2)",
        "image": "images/happy_measure_1.png",
        "first_note": "5",
        "text": "The first note is a G. The highlighted key is a G. Can you play it? Now try playing it! Remember, use your number keys to control the piano.",
        "next_lesson": "2"
    },
    "2": {
        "id": "2",
        "title": "Happy Birthday (measures 3 & 4)",
        "image": "images/happy_measure_2.png",
        "first_note": "6",
        "text": "Highlighted is the note A. Play these two measures.",
        "next_lesson": "3"
    },
    "3": {
        "id": "3",
        "title": "Happy Birthday (measures 5 & 6)",
        "image": "images/happy_measure_3.png",
        "first_note": "w",
        "text": "Highlighted is the high G. Play these two measures.",
        "next_lesson": "4"
    },
    "4": {
        "id": "4",
        "title": "Happy Birthday (measures 7 & 8)",
        "image": "images/happy_measure_4.png",
        "first_note": "0",
        "text": "Highlighted is the first note: high E. Play these two measures.",
        "next_lesson": "end"
    },

    # mary had a little lamb start
    "5": {
        "id": "5",
        "title": "Mary Had A Little Lamb (measures 1 & 2)",
        "image": "images/mary_measure_1.png",
        "first_note": "3",
        "text": "Let’s start with the first verse. The notes are notated for you here. The white note is a half note, that takes twice as long as the black note (quarter note). The first note is an E.",
        "next_lesson": "6"
    },

    "6": {
        "id": "6",
        "title": "Mary Had A Little Lamb (measures 3 & 4)",
        "image": "images/mary_measure_2.png",
        "first_note": "2",
        "text": "Now moving on to the next two measures!",
        "next_lesson": "7"
    },

    "7": {
        "id": "7",
        "title": "Mary Had A Little Lamb (measures 5 & 6)",
        "image": "images/mary_measure_3.png",
        "first_note": "3",
        "text": "Now moving on to the next two measures!",
        "next_lesson": "8"
    },
    "8": {
        "id": "8",
        "title": "Mary Had A Little Lamb (measures 7 & 8)",
        "image": "images/mary_measure_4.png",
        "first_note": "2",
        "text": "Now moving on to the next two measures! The last C is a whole note, which means it lasts four beats.",
        "next_lesson": "9"
    },
    "9": {
        "id": "9",
        "title": "Mary Had A Little Lamb (measures 9-12)",
        "image": "images/mary_measure_5.png",
        "first_note": "3",
        "text": "Now moving on to the next four measures! We already learned this, so this should be pretty easy!",
        "next_lesson": "10"
    },
    "10": {
        "id": "10",
        "title": "Mary Had A Little Lamb (measures 13-16)",
        "image": "images/mary_measure_6.png",
        "first_note": "3",
        "text": "Now moving on to the next fourt measures! We already learned this, so this should be pretty easy!",
        "next_lesson": "end"
    },

}


# ROUTES

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/piano_basics/<step>')
def piano_basics(step):
    lesson = basics.get(step)
    if not lesson:
        return redirect(url_for("piano_basics"))  # or home if you prefer

    return render_template("piano_basics.html", lesson=lesson)

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

@app.route("/learn/<step>")
def learn(step):
    lesson = lessons.get(step)  # or whichever dict you're using (e.g. 'mary_lessons')

    if not lesson:
        return redirect(url_for("song_list"))

    return render_template("learn.html", lesson=lesson)



@app.route('/practice')
def practice():
    song_param = request.args.get("song")

    song_title = {
        "happy_birthday": "Happy Birthday",
        "mary_lamb": "Mary Had a Little Lamb"
    }.get(song_param, None)

    return render_template("practice.html", song_title=song_title)


@app.route("/quiz/<int:index>")
def quiz(index):
    if index >= len(quiz_questions):
        return redirect(url_for('song_list'))

    question = quiz_questions[index]
    return render_template(
        "quiz.html",
        question=question,
        index=index,
        total=len(quiz_questions)
    )



# AJAX FUNCTIONS




if __name__ == '__main__':
   app.run(debug = True, port=5001)





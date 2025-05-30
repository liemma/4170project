from flask import Flask
from flask import request
from flask import render_template
from flask import Response, request, jsonify
from flask import redirect, url_for
from datetime import datetime
app = Flask(__name__, static_folder="static")

quiz_questions = [
    {"image": "missing_note_1.png", "answer": "F4"},
    {"image": "missing_note_2.png", "answer": "C4"},
    {"image": "type_note_1.png", "answer": "half note"},
    {"image": "type_note_2.png", "answer": "quarter note"},
]

activity_log = []
quiz_answers = {}
song_log = []

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
        "next_lesson": "3"
    },
    "3": {
        "id": "3",
        "title": "Types of Notes",
        "image": "images/types_of_notes.png",
        "text": "On sheet music, you’ll see different types of notes.\nEach type determines how many beats you hold the note for.\nThese are the note types you’ll encounter later on.",
        "next_lesson": "4"
    },
    "4": {
        "id": "4",
        "title": "How to Play",
        "image": "",
        "text": "We turned your computer keyboard into a piano keyboard! Your keys in the number row of your keyboard will control the piano keys labeled below. Try it now! \n Let’s review some of what we've learned so far. Use the piano below to answer any note questions.",
        "next_lesson": "quiz"
    }
}

lessons = {
    "1": {
        "id": "1",
        "song_id": "2",
        "title": "Happy Birthday (first measures 1 & 2)",
        "image": "images/happy_measure_1.png",
        "first_note": "5",
        "text": "The first note is a G. The highlighted key is a G. Can you play it? Now try playing it! Remember, use your number keys to control the piano.",
        "next_lesson": "2"
    },
    "2": {
        "id": "2",
        "song_id": "2",
        "title": "Happy Birthday (measures 3 & 4)",
        "image": "images/happy_measure_2.png",
        "first_note": "6",
        "text": "Highlighted is the note A. Play these two measures.",
        "next_lesson": "3"
    },
    "3": {
        "id": "3",
        "song_id": "2",
        "title": "Happy Birthday (measures 5 & 6)",
        "image": "images/happy_measure_3.png",
        "first_note": "w",
        "text": "Highlighted is the high G. Play these two measures.",
        "next_lesson": "4"
    },
    "4": {
        "id": "4",
        "song_id": "2",
        "title": "Happy Birthday (measures 7 & 8)",
        "image": "images/happy_measure_4.png",
        "first_note": "0",
        "text": "Highlighted is the first note: high E. Play these two measures.",
        "next_lesson": "quiz"
    },

    # mary had a little lamb start
    "5": {
        "id": "5",
        "song_id": "1",
        "title": "Mary Had A Little Lamb (measures 1 & 2)",
        "image": "images/mary_measure_1.png",
        "first_note": "3",
        "text": "Let’s start with the first verse. The notes are notated for you here. The white note is a half note, that takes twice as long as the black note (quarter note). The first note is an E.",
        "next_lesson": "6"
    },

    "6": {
        "id": "6",
        "song_id": "1",
        "title": "Mary Had A Little Lamb (measures 3 & 4)",
        "image": "images/mary_measure_2.png",
        "first_note": "2",
        "text": "Now moving on to the next two measures!",
        "next_lesson": "7"
    },

    "7": {
        "id": "7",
        "song_id": "1",
        "title": "Mary Had A Little Lamb (measures 5 & 6)",
        "image": "images/mary_measure_3.png",
        "first_note": "3",
        "text": "Now moving on to the next two measures!",
        "next_lesson": "8"
    },
    "8": {
        "id": "8",
        "song_id": "1",
        "title": "Mary Had A Little Lamb (measures 7 & 8)",
        "image": "images/mary_measure_4.png",
        "first_note": "2",
        "text": "Now moving on to the next two measures! The last C is a whole note, which means it lasts four beats.",
        "next_lesson": "9"
    },
    "9": {
        "id": "9",
        "song_id": "1",
        "title": "Mary Had A Little Lamb (measures 9-12)",
        "image": "images/mary_measure_5.png",
        "first_note": "3",
        "text": "Now moving on to the next four measures! We already learned this, so this should be pretty easy!",
        "next_lesson": "10"
    },
    "10": {
        "id": "10",
        "song_id": "1",
        "title": "Mary Had A Little Lamb (measures 13-16)",
        "image": "images/mary_measure_6.png",
        "first_note": "3",
        "text": "Now moving on to the next four measures! We already learned this, so this should be pretty easy!",
        "next_lesson": "quiz"
    },

}

basics_progress = 0
quiz_progress = 0
learn_progress = 0

def log_user_event(action, data=None):
    timestamp = datetime.utcnow().isoformat()
    entry = {"timestamp": timestamp, "action": action}
    if data:
        entry.update(data)
    activity_log.append(entry)

# ROUTES

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html", about={"title": "About Us"})

@app.route('/piano_basics/<step>')
def piano_basics(step):
    lesson = basics.get(step)

    # Map lesson step to progress value
    step_to_progress = {
        "1": 0,
        "2": 25,
        "3": 50,
        "4": 75
    }
    basics_progress = step_to_progress.get(step, 0)

    if lesson:
        log_user_event("enter_piano_basics", {"step": step})
    return render_template("piano_basics.html", lesson=lesson, basics_progress=basics_progress)


@app.route('/song_list')
def song_list():
    return render_template("song_list.html")

@app.route('/practice_list')
def practice_list():
    return render_template("practice_list.html")

@app.route('/learn_song')
def learn_song():
    song_id = request.args.get("song")
    song = songs.get(song_id)

    if not song:
        return render_template("learn_song.html", song_title=None)

    # map song_id to route param used elsewhere
    song_id_to_param = {
        "1": "mary_lamb",
        "2": "happy_birthday"
    }
    song_param = song_id_to_param.get(song_id)

    if not song_param:
        return redirect(url_for("song_list"))

    return render_template(
        "learn_song.html",
        song_title=song["title"],
        song_image=song["image"],
        song_description=song["description"],
        song_param=song_param
    )


@app.route("/learn/<step>")
def learn(step):
    lesson = lessons.get(step)
    if not lesson:
        return redirect(url_for("song_list"))

    song_id_to_param = {"1": "mary_lamb", "2": "happy_birthday"}
    song_param = song_id_to_param.get(str(lesson.get("song_id")))

    log_user_event("enter_learn_song", {"step": step, "song_id": lesson["song_id"]})

    # Compute progress
    current_song_id = lesson["song_id"]
    song_lessons = [l for l in lessons.values() if l["song_id"] == current_song_id]
    sorted_steps = sorted(song_lessons, key=lambda x: int(x["id"]))
    total_steps = len(sorted_steps)
    current_index = next(i for i, l in enumerate(sorted_steps) if l["id"] == step)
    learn_progress = int((current_index / total_steps) * 100)

    # 👇 Don't redirect until *after* this lesson is rendered
    return render_template(
        "learn.html",
        lesson=lesson,
        song_param=song_param,
        learn_progress=learn_progress
    )




# View activity log
@app.route("/activity_log")
def show_activity_log():
    return jsonify(activity_log)

# View quiz answers
@app.route("/quiz_answers")
def show_quiz_answers():
    return jsonify(quiz_answers)

# View practice results
@app.route("/results")
def practice_results():
    return jsonify(song_log)

@app.route('/practice_intro')
def practice_intro():
    song_param = request.args.get("song")
    
    if not song_param:
        return redirect(url_for('song_list'))

    song_map = {
        "mary_lamb": {
            "title": "Mary Had a Little Lamb",
            "id": "1"
        },
        "happy_birthday": {
            "title": "Happy Birthday",
            "id": "2"
        }
    }

    song_info = song_map.get(song_param)
    if not song_info:
        return redirect(url_for('song_list'))

    return render_template(
        "practice_intro.html",
        song_title=song_info["title"],
        song_param=song_param
    )

@app.route('/practice_play')
def practice_play():
    song_param = request.args.get("song")

    if not song_param:
        return redirect(url_for('song_list'))

    song_map = {
        "mary_lamb": {
            "title": "Mary Had a Little Lamb",
            "id": "1"
        },
        "happy_birthday": {
            "title": "Happy Birthday",
            "id": "2"
        }
    }

    song_info = song_map.get(song_param)
    if not song_info:
        return redirect(url_for('song_list'))

    return render_template(
        "practice_play.html",
        song_title=song_info["title"],
        song_param=song_param
    )


@app.route("/quiz/<int:index>", methods=["GET", "POST"])
def quiz(index):
    global quiz_answers

    if request.method == "POST":
        user_answer = request.form.get("answer")
        if user_answer:
            quiz_answers[str(index)] = {
                "answer": user_answer,
                "timestamp": datetime.now().isoformat()
            }
        return redirect(url_for("quiz", index=index + 1))

    if index >= len(quiz_questions):
        return redirect(url_for('song_list'))

    question = quiz_questions[index]

    # Compute quiz progress
    total_questions = len(quiz_questions)
    quiz_progress = int((index / total_questions) * 100)

    # Determine the appropriate "Next" destination
    if index < len(quiz_questions) - 1:
        next_lesson_url = url_for("quiz", index=index + 1)
    else:
        next_lesson_url = url_for("song_list")


    return render_template(
        "quiz.html",
        question=question,
        index=index,
        total=total_questions,
        quiz_progress=quiz_progress,
        next_lesson_url=next_lesson_url
    )





# AJAX FUNCTIONS
@app.route('/store_practice_result', methods=['POST'])
def store_practice_result():
    data = request.get_json()
    song_log.append({
        "type": "practice_result",
        "song": data["song"],
        "accuracy": data["accuracy"],
        "incorrect_notes": data["incorrect"],
        "timestamp": datetime.now().isoformat()
    })
    return jsonify(success=True)

if __name__ == '__main__':
   app.run(debug = True, port=5001)





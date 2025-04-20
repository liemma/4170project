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


# AJAX FUNCTIONS

# ajax for people.js
@app.route('/add_name', methods=['GET', 'POST'])
def add_name():
    global data 
    global current_id 

    json_data = request.get_json()   
    name = json_data["name"] 
    
    # add new entry to array with 
    # a new id and the name the user sent in JSON
    current_id += 1
    new_id = current_id 
    new_name_entry = {
        "name": name,
        "id":  current_id
    }
    data.append(new_name_entry)

    #send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data = data)
 


if __name__ == '__main__':
   app.run(debug = True, port=5001)





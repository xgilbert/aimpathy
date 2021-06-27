import flask
from flask import request, jsonify, render_template

import spacy

from aimpathy.train import train


DATA_PATH = "../data"
MODEL_PATH = "../model"

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/v1/test', methods=['GET'])
def test():
    nlp = spacy.load("en_core_web_sm")
    nlp_aim = spacy.load(f"{MODEL_PATH}/model.pickle")

    note = "Jan 21: mail John S about signing them up for phase 3 of project Beta."
    
    doc = nlp(note)
    doc_aim = nlp_aim(note)

    # parse note
    contact_name = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    contact_name = " ".join(str(e) for e in contact_name)

    contact_type = [ent.text for ent in doc_aim.ents if ent.label_ == "B-ContType"]
    contact_type = " ".join(str(e) for e in contact_type)

    date = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    date = " ".join(str(e) for e in date)

    project = [ent.text for ent in doc_aim.ents if ent.label_ == "I-ProjName"]
    project = " ".join(str(e) for e in project)

    res = {
        "contact_name": contact_name,
        "contact_type": contact_type,
        "date": date,
        "project": project,
    }

    control = {
        "contact_name": "John S",
        "contact_type": "mail",
        "date": "Jan 21",
        "project": "Beta",
    }

    if res == control:
        res = {
            "status": "spacy and en_core_web_sm loaded successfully",
            "test": "passed"    
        }

    return jsonify(res)


@app.route('/api/v1/train', methods=['GET'])
def train_model():
    train(DATA_PATH, MODEL_PATH, n_iter=10)
    return "<h1>Model successfully trained.</h1>"


@app.route('/api/v1/note', methods=['GET'])
def note():
    if "note" in request.args:
        note = request.args["note"]
    else:
        return "<h1>[ERROR] : Please provide a note to parse.</h1>"

    # load models
    nlp = spacy.load("en_core_web_sm")
    nlp_aim = spacy.load(f"{MODEL_PATH}/model.pickle")

    # instantiate
    doc = nlp(note)
    doc_aim = nlp_aim(note)

    # parse note
    contact_name = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    contact_name = " ".join(str(e) for e in contact_name)

    contact_type = [ent.text for ent in doc_aim.ents if ent.label_ == "B-ContType"]
    contact_type = " ".join(str(e) for e in contact_type)

    date = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    date = " ".join(str(e) for e in date)

    project = [ent.text for ent in doc_aim.ents if ent.label_ == "I-ProjName"]
    project = " ".join(str(e) for e in project)

    res = {
        "contact_name": contact_name,
        "contact_type": contact_type,
        "date": date,
        "project": project,
    }

    return jsonify(res)


app.run()
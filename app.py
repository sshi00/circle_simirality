from flask import Flask,jsonify,request
import yaml
import json
import load_vector
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

with open('config.yml') as f:
    config = yaml.load(f)['server']

with open(config['json_file_path'],'r') as json_file:
    question_data = json.load(json_file)

@app.route('/api/question')
def return_question():
    return jsonify(question_data)

@app.route('/api/similarity',methods=['POST'])
def return_similar():
    json = request.get_json()
    selected_question = json["selected_question"]
    question_data = json["question_data"]

    cred = credentials.Certificate(config['firebase_credential_path'])
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    positive = []
    negative = []

    for idx,selected in enumerate(selected_question):
        if  selected == None:
            continue
        positive.append(question_data[idx]['selection'][selected]['value'])
        negative.append(question_data[idx]['selection'][1-selected]['value'])

    keyword = ','.join(positive)
    similar = dict(load_vector.calcurate_most_similar(keyword))

    circle_name = list(similar.keys())

    result = []

    for circle in circle_name:
        circle_dict = db.collection(u'versions').document(u'v1').collection(u'circles').document(circle).get()
        circle_dict = circle_dict.to_dict()
        result_dict = {"name":circle,"similarity":similar[circle],"twitter_url":circle_dict["twitter_link"],"instagaram_url":circle_dict['instagram_link']}
        result.append(result_dict)


    json["result"] = result
    return jsonify(json)




if __name__ == "__main__":
    app.run(port=config['port'])

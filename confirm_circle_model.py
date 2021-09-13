import MeCab
import yaml
import sys
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from collections import OrderedDict
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

with open('config.yml') as f:
    config = yaml.load(f)['server']

def save_model():
    cred = credentials.Certificate(config['firebase_credential_path'])
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    docs = db.collection(u'versions').document(u'v1').collection(u'circles').stream()
    training_docs = []

    for doc in docs:

        circle_dict =  doc.to_dict()
        circle_twitter = circle_dict['twitter_post']
        circle_google = circle_dict['google_snippet']
        circle_list = circle_twitter + circle_google
    print(doc.id)
    print(circle_list)


# このファイルを直接指定した時に、main関数を呼び出す。
if __name__ == '__main__':
    save_model()

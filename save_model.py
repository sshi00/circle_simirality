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

model_name = sys.argv[1]

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

        training_docs.append(TaggedDocument(words=words(','.join(map(str,circle_list))), tags=[doc.id]))

    model = Doc2Vec(documents=training_docs, min_count=1, dm=1, epochs = 50)
    model.save(model_name)

def words(text):

    """
        文章から単語を抽出
    """
    out_words = []
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    node = tagger.parseToNode(text)

    while node:
        word_type = node.feature.split(",")[0]
        if word_type in ['名詞','形容詞','動詞','記号']:
            out_words.append(node.surface)
        node = node.next
    return out_words

# このファイルを直接指定した時に、main関数を呼び出す。
if __name__ == '__main__':
    save_model()

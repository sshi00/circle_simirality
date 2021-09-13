import MeCab
import re
import yaml
from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec

with open('config.yml') as f:
    config = yaml.load(f)['server']

print('ロード中です')
circle_model = Doc2Vec.load(config['custom_model_path'])

def calcurate_most_similar(keyWord):
    '''
    あらかじめロードされたモデルから、与えられた文章に近いサークルを見つける
    その時に、形態素解析も一緒に行う。
    引数: 分かち書きされる前の文章
    返り値: most_similarで得られる配列 ex: [('hoge', 0.88), ('fuga', 0.7)]
    '''
    keyWords =words(keyWord)

    vector = circle_model.infer_vector(keyWords)
    most_similar = circle_model.docvecs.most_similar([vector])

    return most_similar


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
        if word_type in ['名詞','形容詞','動詞']:
            out_words.append(node.surface)

        node = node.next

    return out_words



if __name__ == '__main__':
    while True:
        keyWord =str(input('あなたにマッチするサークルを提案します。あなたがサークル を決定するときに考慮する要因(例えば、サッカー、合コン、 初心者歓迎、等々)を1つ入力してください。\n要因:'))
        most_similar_list = calcurate_most_similar(keyWord)
        print('以下の10個のサークルを提案します。')
        for i,similarity in enumerate(most_similar_list):
            print('{}{}'.format(i+1,similarity))
        judge = int(input('もう1度行いますか？YES:1/NO:0を入力してください'))
        if judge == 0:
            break

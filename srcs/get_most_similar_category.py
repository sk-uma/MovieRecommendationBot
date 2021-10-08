from gensim.models import KeyedVectors
from get_jp_category import get_jp_category

W2V_PATH = '/root/chatBot/word2vec_model/entity_vector.model.bin'
model = KeyedVectors.load_word2vec_format(W2V_PATH, binary=True)


def get_most_similar_category(word):
    if word not in model:
        return None, None
    category_sets = get_jp_category()
    max_score = 0
    max_score_category = ''
    for category in category_sets['genres']:
        score = model.similarity(word, category['name'])
        if score > max_score:
            max_score = score
            max_score_category = category
        score = model.similarity(word, '[' + category['name'] + ']')
        if score > max_score:
            max_score = score
            max_score_category = category
    return max_score_category, max_score


if __name__ == '__main__':
    print('SF')
    category, cos = get_most_similar_category('SF')
    print(category, cos)
    print('恋愛')
    category, cos = get_most_similar_category('恋愛')
    print(category, cos)
    print('近未来')
    category, cos = get_most_similar_category('近未来')
    print(category, cos)
    print('わくわく')
    category, cos = get_most_similar_category('わくわく')
    print(category, cos)
    print('マーベル')
    category, cos = get_most_similar_category('マーベル')
    print(category, cos)
    print('怖い')
    category, cos = get_most_similar_category('怖い')
    print(category, cos)
    print('MCU')
    category, cos = get_most_similar_category('MCU')
    print(category, cos)
    print('アイアンマン')
    category, cos = get_most_similar_category('アイアンマン')
    print(category, cos)

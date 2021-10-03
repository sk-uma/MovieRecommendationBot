from get_most_similar_category import get_most_similar_category
from parse_using_mecab import parse_using_mecab

def parse_message(message):
    parse = parse_using_mecab(message)
    # print(parse[1])
    max_score = 0
    max_score_category = None
    category = None
    score = None
    for noun in parse[1]:
        category, score = get_most_similar_category(noun)
        if category is not None:
            if max_score < score:
                max_score_category = category
    return parse[0], parse[1], max_score_category

if __name__ == '__main__':
    print(parse_message('サイエンスフィクション'))
    print(parse_message('西部劇'))
    print(parse_message('SFが見たい'))
    print(parse_message('怖い映画'))
    print(parse_message('マーベルの映画が見たいです'))
    print(parse_message('木村拓哉が出ている映画'))
    print(parse_message('木村拓哉が出ているサスペンス映画'))
    print(parse_message('ウィル・スミスが出演する映画'))
    print(parse_message('トム・クルーズが出演する映画'))
    print(parse_message('山本美月と甲本雅裕が出てる怖い映画'))

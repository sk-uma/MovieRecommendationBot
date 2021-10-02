import MeCab
import pandas as pd
import io

HEADER = '表層形,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音\n'


def is_base(row):
    if row['原形'] is not None and row['原形'] != '*':
        return row['原形']
    else:
        return row['表層形']


def parse_important_elem(parse_df):
    names = []
    info = []
    name = ""
    noun = ""
    symbol_buf = ""
    for index, row in parse_df.iterrows():
        if row['品詞'] == '記号':
            if name != "" or noun != "":
                symbol_buf = row['表層形']
        else:
            symbol_buf = ""
        if row['品詞'] == '名詞' and \
           row['品詞細分類1'] == '固有名詞' and \
           row['品詞細分類2'] == '人名':
            if name != "":
                name = name + symbol_buf
            name = name + row['表層形']
        else:
            if name != "":
                names.append(name)
            name = ""
        if row['品詞'] == '形容詞':
            info.append(is_base(row))
        if row['品詞'] == '名詞' and \
           row['品詞細分類2'] != '人名':
            if noun != "":
                noun = noun + symbol_buf
            noun = noun + is_base(row)
        else:
            if noun != "" and noun not in ['映画', '出演']:
                info.append(noun)
            noun = ""
    if name != "":
        names.append(name)
    if noun != "" and noun not in ['映画', '出演']:
        info.append(noun)
    return names, info


def parse_sentence_using_mecab(sentence):
    mecab = MeCab.Tagger("")
    parse = mecab.parse(sentence).replace('\t', ',')[:-4]
    parse_df = pd.read_csv(io.StringIO(HEADER + parse))
    names, info = parse_important_elem(parse_df)
    return names, info


def parse_using_mecab(message):
    names = []
    info = []
    for line in message.splitlines():
        names_tmp, info_tmp = parse_sentence_using_mecab(line)
        names = names + names_tmp
        info = info + info_tmp
    return names, info


if __name__ == '__main__':
    print(parse_using_mecab('サイエンスフィクション'))
    print(parse_using_mecab('西部劇'))
    print(parse_using_mecab('SFが見たい'))
    print(parse_using_mecab('怖い映画'))
    print(parse_using_mecab('マーベルの映画が見たいです'))
    print(parse_using_mecab('木村拓哉が出ている映画'))
    print(parse_using_mecab('木村拓哉が出ているサスペンス映画'))
    print(parse_using_mecab('ウィル・スミスが出演する映画'))
    print(parse_using_mecab('トム・クルーズが出演する映画'))
    print(parse_using_mecab('山本美月と甲本雅裕が出てる怖い映画'))
    print(parse_using_mecab('''山本美月
と
甲本雅裕が出てる怖い映画'''))

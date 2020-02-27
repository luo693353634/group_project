


def get_name_score(word, name2id):
    score = 0
    if word in name2id.keys():
        score = 1
    return score
def get_qaly_data(filepath):
    qaly_scorer = {}
    with open(filepath, 'r') as infile:
        for linenum, line in enumerate(infile):
            if linenum == 0:
                continue

            topic, score, keywords, ref = line.split(',')
            keywords = keywords.split(' AND ')
            keywords = tuple([i.strip() for i in keywords]) # remove whitespace

            qaly_scorer[keywords] = (float(score), topic)

    return qaly_scorer

def score_article(article, qaly_scorer):
    article_score = 0

    for keyword_set in qaly_scorer:
        if all(keyword in article for keyword in keyword_set):
            article_score += qaly_scorer[keyword_set][0]

    return article_score

def score_all(article_dict, qaly_scorer):
    for article_url in article_dict:
        article_content = article_dict[article_url]
        article_score = score_article(article_content, qaly_scorer)

        article_dict[article_url] = [article_score, article_content]

    return article_dict

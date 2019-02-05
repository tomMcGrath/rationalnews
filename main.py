import get_articles
import keyword_parser
import calc_qualys
import score_articles
import pickle
import get_whole_article

## Get articles from NewsAPI
"""
page_limit_per_request = 1
results_per_page = 20
article_dict = get_articles.get_results(page_limit_per_request,
                                        results_per_page)

pickled_file = open('dict_url_desc_out.pkl', 'rb')
article_dict = pickle.load(pickled_file)
"""
article_dict = get_whole_article.get_results()

## Calculate aggregate QALY scores for each article
qaly_path = 'global_prios/global_prios_simple.csv'
qaly_scorer = score_articles.get_qaly_data(qaly_path)
article_dict = score_articles.score_all(article_dict, qaly_scorer)
for i in sorted(article_dict, key=lambda x: article_dict[x][0]):
    print(i, article_dict[i])

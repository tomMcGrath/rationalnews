import get_articles
import keyword_parser
import calc_qualys

## Get articles from NewsAPI
page_limit_per_request = 5
results_per_page = 20
article_dict = get_articles.get_results(page_limit_per_request,
                                        results_per_page)

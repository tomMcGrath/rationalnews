import requests
import pickle

# def get_n_results():
#     url = ('https://newsapi.org/v2/everything?'
#     'sources=bbc-news&'
#     'apiKey=9d2e6fa594ef4c6c9d030886d5322618')
#     response = requests.get(url)
#     js = response.json()
#     return js['totalResults']
#npages = int(get_n_results()/20)



dict_url_desc = {}
for i in range(50):
    try:
        if i % 10 == 0:
            print(i)
        p = i + 1
        page_str = 'page={}&'.format(p)
        query = ('https://newsapi.org/v2/everything?sources=bbc-news&'
                 +page_str+
                 'sort=date_published&'
                 'apiKey=9d2e6fa594ef4c6c9d030886d5322618')
        response = requests.get(query)
        js = response.json()
        for k in range(20):
            article = js['articles'][k]
            desc = article['description']
            content = article['content']
            url = article['url']
            if content is not None:
                dict_url_desc[url] = desc + ' ' + content
            else:
                dict_url_desc[url] = desc
            #break
    except KeyError:
        break

dict_url_desc_out = open('dict_url_desc_out.pkl','wb')
pickle.dump(dict_url_desc, dict_url_desc_out)
dict_url_desc_out.close()

import threading, time, datetime
import get_articles, score_articles
import pickle
import numpy as np
from pdb import set_trace
# Class for repetitive actions
class RepeatEvery(threading.Thread):
    """
    Class to repeat a function, with arguments, with a given periodicity

    Parameters
    -----------------
    interval : A float, the amount of time in seconds between calling the function
    func : A function to be called repetitively
    *args : Positional arguments for func
    *kwargs : Named arguments for func
    """
    def __init__(self, interval, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.interval = interval  # seconds between calls
        self.func = func          # function to call
        self.args = args          # optional positional argument(s) for call
        self.kwargs = kwargs      # optional keyword argument(s) for call
        self.runable = True
    def run(self):
        while self.runable:
            self.func(*self.args, **self.kwargs)
            time.sleep(self.interval)
    def stop(self):
        self.runable = False

def tweet_news(tweepyapi,qaly_path,error_log_filename, error_log_pointer, load_articles = False, qaly_thresh = 1.0):
    """
    Tweet a single news story drawn randomly, weighted by a QALY

    Parameters
    --------------
    tweepyapi : tweepy.api.API object, contains Twitter API credentials and allows tweeting
    qaly_path : A string, directory of the QALY table
    error_log_filename : A string, file name for error log
    error_log_pointer : An IO pointer, the pointer to the error log
    load_articles : A bool, if true, load a database of URLs
    qaly_thresh : A float, threshold on qalys to tweet
    """
    if load_articles:
        pickled_file = open('dict_url_desc_out.pkl', 'rb')
        article_dict = pickle.load(pickled_file)
    else:
        # page_limit_per_request = 1
        # results_per_page = 20
        # article_dict = get_articles.get_results()
        article_dict = get_articles.get_results()
    if len(article_dict) < 5: # assume something went wrong and load
        error_log_pointer = open(error_log_filename,'a')
        error_log_pointer.write('get_articles() error,'+str(datetime.datetime.now())+'\n')
        error_log_pointer.close()
        print('Error in get_articles()\n')
    else:
        ## Calculate aggregate QALY scores for each article
        # BUG: score_articles.get_qaly_data fails for the trivial case of X AND Y AND Z
        qaly_scorer = score_articles.get_qaly_data(qaly_path)
        article_dict = score_articles.score_all(article_dict, qaly_scorer)

        v = article_dict.values()
        v = list(v)
        qalys_scores = np.array([ a for a,b in v ] )
        qaly_total = qalys_scores.sum()
        if qaly_total < qaly_thresh: # there aren't enough newsworthy stories
            output=tweepyapi.update_status("I didn't find anything interesting at " + str(datetime.datetime.now()))
            error_log_pointer = open(error_log_filename,'a')
            error_log_pointer.write("No news"+','+str(datetime.datetime.now())+'\n')
            error_log_pointer.close()
            print('No news\n')
            return
        article_choice_index = np.random.choice(len(qalys_scores), p=qalys_scores/qalys_scores.sum())
        url = list(article_dict.keys())[article_choice_index]

        #set_trace()
        try:
            output=tweepyapi.update_status(url)
            error_log_pointer = open(error_log_filename,'a')
            error_log_pointer.write('Success,'+str(datetime.datetime.now())+'\n')
            error_log_pointer.close()
        except Exception as e:
            # To do: this is bad practice, shouldn't catch all possible exceptions
            error_log_pointer = open(error_log_filename,'a')
            error_log_pointer.write(e.reason+','+str(datetime.datetime.now())+'\n')
            error_log_pointer.close()
    print('Done!')

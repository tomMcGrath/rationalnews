import threading, time, datetime
import get_articles, score_articles
import pickle
import numpy as np
from pdb import set_trace
import sqlite3 as sq
import os

def create_db(db_filename, create_str):
    """ Create a SQLite database

    Parameters
    ----------------
    db_filename : A string, the name of the database to create
    """
    if not os.path.exists(db_filename):
        conn = sq.connect(db_filename)
        c = conn.cursor()
        c.execute(create_str)
        conn.commit()
        conn.close()

def save_news(db_filename, article_dict):
    ''' Insert article_dict into news

    P

    '''
    a=1

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

def tweet_news(tweepyapi,qaly_path,error_log_filename, error_log_pointer, load_articles = False, qaly_thresh = 1.0, sample_log_qalys=True, dbg_mode=False):
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
    sample_log_qalys : A bool, sample the qalys in log-space
    dbg_mode : A bool, enter debug mode. Samples fewer pages from the API, since we have a daily budget
    """
    if load_articles:
        pickled_file = open('dict_url_desc_out.pkl', 'rb')
        article_dict = pickle.load(pickled_file)
    else:
        if dbg_mode:
            article_dict = get_articles.get_results(page_limit_per_request = 1)
        else:
            article_dict = get_articles.get_results()
        save_news()
    if len(article_dict) < 5: # assume something went wrong with the API
        output=tweepyapi.update_status("Something went wrong with the API at " + str(datetime.datetime.now()))
        error_log_pointer = open(error_log_filename,'a')
        error_log_pointer.write('get_articles() error,'+str(datetime.datetime.now())+',NaN'+'\n')
        error_log_pointer.close()
        print('Error in get_articles()\n')
        return
    else:
        ## Calculate aggregate QALY scores for each article
        qaly_scorer = score_articles.get_qaly_data(qaly_path)
        article_dict = score_articles.score_all(article_dict, qaly_scorer)
        v = article_dict.values()
        v = list(v)
        qalys_scores = np.array([ a[0] for a in v ] )
        qaly_total = qalys_scores.sum()
        if qaly_total < qaly_thresh: # there aren't enough newsworthy stories
            output=tweepyapi.update_status("I didn't find anything interesting at " + str(datetime.datetime.now()))
            error_log_pointer = open(error_log_filename,'a')
            error_log_pointer.write("No news"+','+str(datetime.datetime.now())+',NaN'+'\n')
            error_log_pointer.close()
            print('No news\n')
            return
        if sample_log_qalys:
            qalys_scores = np.log(qalys_scores + 1.0) # sample qalys in log-space

        article_choice_index = np.random.choice(len(qalys_scores), p=qalys_scores/qalys_scores.sum())
        url = list(article_dict.keys())[article_choice_index]
        topics = v[article_choice_index][2]
        topics_string = ''
        for i, topic in enumerate(topics):
            if i == len(topics) - 1:
                topics_string+=topic
            else:
                topics_string+=topic+'; '
        try:
            output=tweepyapi.update_status(topics_string + '\n' + url)
            error_log_pointer = open(error_log_filename,'a')
            error_log_pointer.write('Success,'+str(datetime.datetime.now())+','+topics_string+'\n')
            error_log_pointer.close()
        except Exception as e:
            output=tweepyapi.update_status(e.reason+' Time: '+ str(datetime.datetime.now()))
            error_log_pointer = open(error_log_filename,'a')
            error_log_pointer.write(e.reason+','+str(datetime.datetime.now())+',NaN'+'\n')
            error_log_pointer.close()
            print(e.reason)
            return
    print('Done!')

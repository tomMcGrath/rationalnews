import numpy as np
import get_articles
import keyword_parser
import calc_qualys
import score_articles
import pickle
#import get_whole_article
import tweepy
import datetime
import time, threading
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

def tweet_news(tweepyapi,qaly_path,error_log_filename, error_log_pointer, load_articles = False):
    """
    Tweet a single news story drawn randomly, weighted by a QALY

    Parameters
    --------------
    tweepyapi : tweepy.api.API object, contains Twitter API credentials and allows tweeting
    qaly_path : A string, directory of the QALY table
    error_log_filename : A string, file name for error log
    error_log_pointer : An IO pointer, the pointer to the error log
    load_articles : A bool, if true, load a database of URLs
    """
    if load_articles:
        pickled_file = open('dict_url_desc_out.pkl', 'rb')
        article_dict = pickle.load(pickled_file)
    else:
        page_limit_per_request = 1
        results_per_page = 20
        article_dict = get_articles.get_results(page_limit_per_request,
                                                results_per_page)
    if len(article_dict) < 5: # assume something went wrong and load
        error_log_pointer = open(error_log_filename,'a')
        error_log_pointer.write('Error 1,'+str(datetime.datetime.now())+'\n')
        error_log_pointer.close()
    else:
        ## Calculate aggregate QALY scores for each article
        # BUG: score_articles.get_qaly_data fails for the trivial case of X AND Y AND Z
        qaly_scorer = score_articles.get_qaly_data(qaly_path)
        article_dict = score_articles.score_all(article_dict, qaly_scorer)

        v = article_dict.values()
        v = list(v)
        qalys_scores = np.array([ a for a,b in v ] )
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

credentials_dir = '../'
credentials_filename = 'twitter_API_keys.txt' # this must be placed in the directory above the repo

# Parse twitter credentials from the text file, see https://developer.twitter.com/en/apps
fp = open(credentials_dir+credentials_filename,'r')
creds = fp.read().splitlines()
for c in creds:
    if 'API_key=' in c:
        consumer_token=c.split('=')[1]
    if 'API_secret_key=' in c:
        consumer_secret=c.split('=')[1]
    if 'Access_token=' in c:
        access_token=c.split('=')[1]
    if 'Access_token_secret=' in c:
        access_token_secret=c.split('=')[1]

# Set twitter credentials
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
tweepyapi = tweepy.API(auth)

qaly_path = 'global_prios/global_prios.csv'

# Set up error log
error_log_filename = 'error_log.txt'
error_log_pointer = open(error_log_filename,'w')
error_log_pointer.write('Type,Time\n')
error_log_pointer.close()

periodicity_s = 3600
max_time = 7*24*3600

thread = RepeatEvery(periodicity_s, tweet_news, tweepyapi, qaly_path, error_log_filename, error_log_pointer)

print('Starting')
thread.start()
thread.join(max_time)
thread.stop()
print('Stopped')

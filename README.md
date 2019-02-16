# rationalnews
Systems &amp; Signals group project for rationally-reported news

The function calculateURLQUALYs in `calc_qualys.py` takes as input a Pandas DataFrame where the rows are the URLs of articles and the columns are topics and elements greater than zero denote that the article is about that topic and the name of CSV file containing a list of topics and the QALYs associated with that topic. The function outputs a dictionary of the urls and the QALYs associated with the topic of the article. If an article is about multiple topics the QALYs are summed.

```
ssh ratnews # ssh into the EC2 instance
tmux attach # if there are any running sessions
```
If there are running sessions, you will see the output. Otherwise, to run the script

```
tmux
cd rationalnews
python main.py
```
then `ctrl+b d` to detach the tmux session, and `ctrl+d` to log out of the EC2 instance

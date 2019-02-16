1. Make an account with http://aws.amazon.com and go to https://eu-west-1.console.aws.amazon.com/console/home?region=eu-west-1#
2. Click on Instances and Launch Instance
3. Follow the steps, make an Ubuntu 18.04 instance with t2.micro (free tier)
4. Note the Public DNS, and ssh into the instance (see https://www.youtube.com/watch?v=l53QjtPvF_A)
5. Then, inside the instance:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo apt-get autoclean
wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
bash Anaconda3-2018.12-Linux-x86_64.sh
```

Make sure

`export PATH="/home/ubuntu/anaconda3/bin:$PATH"`

```
source .bashrc
rm Anaconda3-2018.12-Linux-x86_64.sh
git clone https://github.com/tomMcGrath/rationalnews.git
sudo apt-get install ruby-dev
sudo gem install twurl
easy_install tweepy
```

6. Go to https://developer.twitter.com/en/apply-for-access and make a developer account. For the Callback URL, put anything e.g. http://wwwf.imperial.ac.uk/~nsjones/jones.htm. When you have a consumer key and a consumer private key

```
twurl authorize --consumer-key key       \
                --consumer-secret secret
```
Open the URL that is printed out, copy the PIN and paste back into the terminal.

7. To tweet
```
twurl -d 'status=Testing twurl' /1.1/statuses/update.json
```

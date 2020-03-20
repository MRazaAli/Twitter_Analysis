import pymongo
import json
import tweepy
import validation as v

class TwitterStreamer():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    # streaming with keyword, in this case the trends.
    def filtering(self, keywords):
        self.stream.filter(track=keywords, languages=['en'])

    def no_filtering(self):
        self.stream.sample(languages=['en'])



class TwitterListener(tweepy.StreamListener):

    def on_data(self, data):
        self.data_process(data)
        print("tweet")
        return True

    def data_process(self, data):

        try:
            # save tweet in the variable tweet.
            tweet = json.loads(data)

            #.Select the data form the tweet and store it in the tweet_collection

            userid = tweet['id']
            user = tweet['user']['screen_name']
            language = tweet['lang'] # language should be english
            retweeted = tweet['retweeted']
            mentions = tweet['entities']['user_mentions']
            reply_to = tweet['in_reply_to_screen_name'] # replying to
            quote = tweet['is_quote_status']
            text = tweet['text'] # text used
            hashtags = tweet['entities']['hashtags'] # Hashtags included in the tweet
            formatTweet ={'id': userid, 'username': user, 'text': text, 'hashtags': hashtags, 'language': language,
                           'mentions': mentions, 'reply_to': reply_to, 'quote': quote, 'retweeted': retweeted}
            print(formatTweet)
            tweet_collection.insert(formatTweet)

        except BaseException:
            pass

    def on_error(self, status):
        # Returning False on_data method in case rate limit occurs.
        if status == 420:
            return False
        if status == 11000:
            print(status)


"Shows the 10 most recent trends on twitter in the UK"
def search_trending(api):

    trends = api.trends_place(23424975)[0]["trends"]  #UKs location
    list_of_trends = [t["name"] for t in trends]
    print(list_of_trends[:10])
    return (list_of_trends[:10])


class Node():
    def __init__(self, user_name):
        self.user_name = user_name
        self.link = None
        # for tweets
        self.friends_name = {}
        self.tweets = []

        # for retweets/ quotes and replies

        self.retweets = []
        self.edges = {}  # for retweets and quotes replies

    def get_link(self):
        return self.link

    def set_friends(self, friend_username):
        if friend_username not in self.friends_name:
            self.friends_name[friend_username] = 1
        else:
            self.friends_name[friend_username] = self.friends_name[friend_username] + 1

    def show_friend_n_freq(self):
        for friend_username in self.friends_name:
            return print(str(friend_username) + ' frequeny : ' + str(self.friends_name[friend_username]))
        else:
            return print(str(friend_username) + ' not mentioned')

    def show_username(self):
        return self.friends_name

    def enter_user_tweets(self, tweet):
        self.tweets.append(tweet)

    def enter_user_retweets(self, retweet):
        self.retweets.append(retweet)

    def set_node_edges(self, friend_username):
        if friend_username not in self.edges:
            self.edges[friend_username] = 1
        else:
            self.edges[friend_username] = self.edges[friend_username] + 1


class Graph():
    def __init__(self):
        self.Nodes = {}

    def make_node(self, user_name):
        node = Node(user_name)
        self.Nodes[user_name] = node

    def enter_node_friends(self, user_name, friends):
        #         first search the user_name from node

        if user_name in self.Nodes:
            self.Nodes[user_name].set_friends(friends)
        else:
            print('user not entered')

    def show_friend_n_freq(self, user_name):
        if user_name in self.Nodes:
            self.Nodes[user_name].show_friend_n_freq()
        else:
            print('user not entered')

    def enter_node_tweets(self, user_name, tweet):
        if user_name in self.Nodes:
            self.Nodes[user_name].enter_user_tweets(tweet)
        else:
            print('user not entered')

    def enter_node_retweets(self, user_name, tweet):
        #         for retweets, replies and quotes
        if user_name in self.Nodes:
            self.Nodes[user_name].enter_user_retweets(tweet)
        else:
            print('user not entered')

    def get_tweets(self, user_name):
        if user_name in self.Nodes:
            return self.Nodes['user_name'].tweets
        else:
            print('user not entered')

    def get_retweets(self, user_name):
        if user_name in self.Nodes:
            return self.Nodes['user_name'].retweets
        else:
            print('user not entered')


if __name__ == "__main__":

    # Database linking
    client = pymongo.MongoClient('localhost', 27017)
    db = client.WebScience
    tweet_collection = db.tweet_collection
    tweet_collection.create_index([("id", pymongo.ASCENDING)], unique=True, dropDups=True)

    #create the listener
    tweet_listener = TwitterListener()

    # This handles Twitter authentification and the connection to Twitter Streaming API
    auth = tweepy.OAuthHandler(v.CONSUMER_KEY, v.CONSUMER_SECRET)
    auth.set_access_token(v.ACCESS_TOKEN, v.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # searching for trends
    keywords = search_trending(api)
    stream = TwitterStreamer(auth, tweet_listener)


    # Either get trending related tweets or without trending.
    option = False
    while option == False:
        try:
            options = input("Get trending topic tweets? ")
            if options.lower() == "yes":
                #streaming with trends
                stream.filtering(keywords)
                option == True
            elif options.lower() == "no":
                #sample streaming
                stream.no_filtering()
                option == True
        except ValueError:
            print("Incorrect input, answer with yes or no please.")

    print("Tweets are loading now.....")

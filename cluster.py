import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


'''
This program takes a while to run on larger datasets
But it's worth it!
'''


def getTweetText(tweet_collection):

    #initialising empty lists to later store information.
    user_names = []
    hashtags = []
    text = []
    alldata = tweet_collection.find()

    # extracting the username, hashtags and text from the data and adding them to the lists
    # defined above.
    for tweet in alldata:
        username_tweets = str(tweet['username']).lower()
        hashtags_tweets = str(tweet['hashtags']).lower()
        tweet_text = str(tweet['text']).lower()
        user_names.append(username_tweets)
        hashtags.append(hashtags_tweets)
        text.append(tweet_text)

    return user_names, hashtags, text



def top_results(vectorizer, group):
    k = 6
    centroids = group.cluster_centers_.argsort()[:, ::-1]
    text = vectorizer.get_feature_names()
    for c in range(k):
        print("CLUSTER %d:" % c)
        for i in centroids[c, :5]:
            print(' %s' % text[i])


def clustering(user_names, hashtags, texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    k = 6

    vector_user_names = vectorizer.fit_transform(user_names)
    vector_hashtags = vectorizer.fit_transform(hashtags)
    vector_texts = vectorizer.fit_transform(texts)
    user_namesK = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
    user_namesK.fit(vector_user_names)
    hashtagsK = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
    hashtagsK.fit(vector_hashtags)
    textK = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
    textK.fit(vector_texts)

    return vectorizer, user_namesK, hashtagsK, textK



if __name__ == "__main__":

    # Setting up connection
    client = pymongo.MongoClient('localhost', 27017)
    db = client.WebScience
    tweet_collection = db.tweet_collection

    userNames, hashTags, Texts = getTweetText(tweet_collection)
    vector, user_names_K, hashtags_K, texts_K = clustering(userNames, hashTags, Texts)

    #Getting top results of usernames
    print("USERNAME CLUSTERS:")
    top_results(vector, user_names_K)

    #Getting top results of hashtags
    print("HASHTAG CLUSTERS:")
    top_results(vector, hashtags_K)

    #Getting top results of texts
    print("TEXT CLUSTERS:")
    top_results(vector, texts_K)
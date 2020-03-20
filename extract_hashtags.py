import pymongo
import csv

client = pymongo.MongoClient('localhost', 27017)
db = client.WebScience
tweet_collection = db.tweet_collection
tweets = tweet_collection.find()

hashtags = []


if __name__ == "__main__":

    print("Extract Hashtags")
    for tweet in tweets:
        try:
            tags_of_tweets = ""
            for tag in tweet['hashtags']:
                if tags_of_tweets == "":
                    tags_of_tweets = tag['text']
                else:
                    tags_of_tweets = tags_of_tweets + " " + tag['text']
            if tags_of_tweets != "":
                hashtags.append(tags_of_tweets)
        except:
            pass

    print(hashtags)

    print("Write to CSV File")

    with open('hashtags.csv', 'w', newline='') as f:
        # creating a writer to write to csv.
        w = csv.writer(f)
        w.writerow(['hashtags'])
        for e in hashtags:
            w.writerow([e])

    print("Finished")

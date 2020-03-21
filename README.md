# Twitter_Analysis

Web Science AE 2020, University fo Glasgow

1. twitter_crawler.py gets tweets and stores them in a database locally, the name and host may need to be changed depending on your system.

2. twitter_data.csv has all the data, which was streamed for about 1 hour.

3. validation.py has the necessary tokens to connect to my twitter account.

4. clustering.py clusters data by top usernames, hashtags and text.. The data from twitter_data.csv was used to dispaly clusters by connecting to mongodb.

5. clusters.txt has the different clusters extracted.

6. extract_hashtags.py gets hashtags from the data and saves into csv, but can be modified.

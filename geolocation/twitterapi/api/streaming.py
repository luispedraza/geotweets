# Este archivo obtiene datos de la api de twitter y los guarda en mongodb

from __future__ import absolute_import, print_function

import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

CONSTANTS = {
    "consumer_key": "p9sppPuAT4RcQQTK6gEGg2iMH",
    "consumer_secret": "TBVxf8OXXzR2yRYXrA0xWEpddXZrC8fMkt2WkHLAfQIaTAGe0f",
    "access_token": "10722802-jyCskSWwMCWzoY6KXBGy7iNdnq5eNSQ5P9OI8dWhX",
    "access_token_secret": "0jCE2pl62wgi98ukIEeThQTyxj4CP8iRnzppFX7PVLs87",
}

hashtags = ["#Feliz2021", "Adios2020", "2020", "2021", "#FelizNocheVieja", "#FelizAño", "#HappyNewYear", "#Happy2020"]
barcelonaLocations = [1.92, 41.22, 2.18, 41.45]
globalLocations = [-180, -90, 180, 90]

mongoClient = MongoClient(host='localhost', port=27017)

db = mongoClient.mydb
testDB = db.geotutorial

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after

consumer_key = CONSTANTS["consumer_key"]
consumer_secret = CONSTANTS["consumer_secret"]

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = CONSTANTS["access_token"]
access_token_secret = CONSTANTS["access_token_secret"]


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        jsonData = json.loads(data)
        if jsonData.get('geo') is not None:
            # save geolocated tweets
            print("Saving data...")
            id = testDB.insert(jsonData)
            print(id)
            print(jsonData)
        else:
            #print("There's nothing to be saved")
            pass

        return True

    def on_status(self, status):
        return True

    def on_error(self, status):
        print("error: ")
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    # stream.filter(track=hashtags)
    # twits en la zona de barcelona:
    # stream.filter(locations=globalLocations, track=hashtags)
    #stream.filter(track=hashtags)
    stream.filter(locations=globalLocations)

from collections import OrderedDict
import hug
from rocketchat_API.rocketchat import RocketChat

from textblob_de import TextBlobDE as TextBlob

import config

rocket = RocketChat(config.BAHN_BOT_NAME, config.BAHN_BOT_PW,
                    server_url='http://10.82.132.65')


def channel_messages(rocket, channel_name):
    json_result = rocket.channels_history(channel_name).json()
    return json_result


def active_users(channel_name):
    cm = channel_messages(rocket, channel_name)['messages']
    users = [x["u"] for x in cm]
    usernames = set([item["username"] for item in users])
    users_information = {"count": len(
        usernames), "usernames": usernames, "activity": "high"}
    return users_information


@hug.get('/sentiment')
def sentiment(channel_name):
    # return polarity in the range [-1.0, 1.0]
    cm = channel_messages(rocket, channel_name)['messages']
    messages = " ".join(x["msg"] for x in cm)
    blob = TextBlob(messages)
    return {"polarity": blob.sentiment.polarity}


@hug.get('/trending')
def trending(channel_name):
    # return polarity in the range [-1.0, 1.0]
    cm = channel_messages(rocket, channel_name)['messages']
    messages = " ".join(x["msg"] for x in cm)
    blob = TextBlob(messages)
    return {"trending topics": sorted(blob.word_counts.items(),
                                      key=lambda t: t[1], reverse=True)}


@hug.get('/messages')
def ch_messages(channel_name: hug.types.text):
    return channel_messages(rocket, channel_name)


@hug.get('/passengers')
def passenger_info(channel_name: hug.types.text):
    au = active_users("GENERAL")
    return au


@hug.get('/technik')
def technik(train_id: hug.types.number):
    problems = {"entity": "Klimaanlage", "status": "kaputt"}
    return problems

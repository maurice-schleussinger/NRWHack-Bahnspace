import hug
from rocketchat_API.rocketchat import RocketChat
import config

rocket = RocketChat(config.BAHN_BOT_NAME, config.BAHN_BOT_PW, server_url='http://10.82.132.65')

def channel_messages(rocket, channel_name):
    json_result = rocket.channels_history(channel_name).json()
    return json_result

def active_users(channel_name):
    cm = channel_messages(rocket, channel_name)['messages']
    users = [x["u"] for x in cm]
    usernames = set([item["username"] for item in users])
    users_information = {"count":len(usernames), "usernames":usernames, "activity":"high"}
    return users_information

@hug.get('/messages')
def ch_messages(channel_name: hug.types.text):
    return channel_messages(rocket, channel_name)

@hug.get('/passengers')
def passenger_info(channel_name: hug.types.text):
    au = active_users("GENERAL")
    return au

@hug.get('/technik')
def technik(train_id: hug.types.number):
    problems = {"entity":"Klimaanlage", "status":"kaputt"}
    return problems
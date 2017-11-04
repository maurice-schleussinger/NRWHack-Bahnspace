from rocketchat_API.rocketchat import RocketChat
import config

rocket = RocketChat(
    'testbot', 'D2PcQ9yCs&MXB8k', server_url='http://10.82.132.65')
pprint(rocket.me().json())
pprint(rocket.chat_post_message('good news everyone!',
                                channel='GENERAL', alias='RE7').json())
pprint(rocket.channels_history('GENERAL', count=5).json())

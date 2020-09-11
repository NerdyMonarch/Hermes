import getjson

class Receiver:
    def __init__(self, pycord, groupme):
        self.pycord = pycord
        self.groupme = groupme
    
    def group_me_to_discord(self, msgs):
        for chat in msgs:
            json = getjson.get_json()
            if not len(json['GroupMe'][chat]['channel_id']) > 0:
                name = json['GroupMe'][chat]['name']
                json['GroupMe'][chat]['channel_id'] = self.pycord.create_channel(name, 'GroupMe')
                getjson.update_json(json)
            channel_id = json['GroupMe'][chat]['channel_id']
            print(channel_id)
            new_msgs = msgs[chat]
            for message in new_msgs:
                print(message)
                user = message['name']
                msg = message['text']
                avatar = message['avatar']
                self.pycord.send_msg(channel_id, user, msg, avatar)
    
    def run(self):
        while self.pycord.is_running():
            if self.pycord.is_connected():
                msgs = self.groupme.get_msgs()
                self.group_me_to_discord(msgs)
            
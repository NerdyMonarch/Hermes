from groupy import Client
import getjson

class PyGroupMe:
    def __init__(self, token):
        self.token = token
        self.client = Client.from_token(token)
        self.json = getjson.get_json()
    
    def get_chat_msgs(self):
        chats = list(self.client.chats.list_all())
        known_chats = list(self.json["GroupMe"].keys())
        msgs = {}
        for chat in chats:
            if chat.other_user['id'] not in known_chats:
                self.json["GroupMe"][chat.other_user['id']] = {
                    'id': chat.other_user['id'],
                    'name': chat.other_user['name'],
                    'type': 'chat',
                    'last_msg': '',
                    'channel_id': ''
                }
            last_msg_id = self.json["GroupMe"][chat.other_user['id']]['last_msg']
            new_msgs = []
            if len(last_msg_id) > 0:
                new_msgs = list(chat.messages.list_since(last_msg_id).autopage())[::-1]
            else:
                new_msgs = list(chat.messages.list().autopage())[::-1]
            if len(new_msgs) > 0:
                msgs[chat.other_user['id']] = []
                for msg in new_msgs:
                    msgs[chat.other_user['id']].append({
                        'name': msg.name,
                        'avatar': msg.avatar_url,
                        'text': msg.text
                    })
                self.json["GroupMe"][chat.other_user['id']]['last_msg'] = new_msgs[0].id
        getjson.update_json(self.json)
        return msgs
    
    def get_group_msgs(self):
        groups = list(self.client.groups.list_all())
        known_groups = list(self.json["GroupMe"].keys())
        msgs = {}
        for group in groups:
            if group.id not in known_groups:
                new_chats = True
                self.json["GroupMe"][group.id] = {
                    'id': group.id,
                    'name': group.name,
                    'type': 'group',
                    'last_msg': '',
                    'channel_id': ''
                }
            last_msg_id = self.json["GroupMe"][group.id]['last_msg']
            new_msgs = []
            if len(last_msg_id) > 0:
                new_msgs = list(group.messages.list_since(last_msg_id).autopage())[::-1]
            else:
                new_msgs = list(group.messages.list().autopage())[::-1]
            if len(new_msgs) > 0:
                msgs[group.id] = []
                for msg in new_msgs:
                    msgs[group.id].append({
                        'name': msg.name,
                        'avatar': msg.avatar_url,
                        'text': msg.text
                    })
                self.json["GroupMe"][group.id]['last_msg'] = new_msgs[0].id
        getjson.update_json(self.json)
        return msgs
    
    def get_msgs(self):
        msgs = self.get_chat_msgs()
        msgs.update(self.get_group_msgs())
        return msgs
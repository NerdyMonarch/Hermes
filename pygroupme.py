from groupy.client import Client

class GroupMeChat:
    def __init__(self, chat, is_group):
        self.is_group = is_group
        if self.is_group:
            self.chat = chat
            self.name = chat.name
        else:
            self.chat = chat
            self.name = chat.other_user['name']
        self.channel = None
        self.last_msg = None

    def get_msgs(self):
        msgs = list(self.chat.messages.list(since_id=self.last_msg))
        if len(msgs) > 0:
            self.last_msg = msgs[0].id
            msgs = msgs[::-1]
        return msgs

class PyGroupMe:
    def __init__(self, token):
        self.token = token
        self.client = Client.from_token(token)
        self.chats = []
        self.groups = []
        self.need_channels = []

    def update_chats(self):
        chats = list(self.client.chats.list().autopage())
        if len(chats) != len(self.chats):
            for chat in self.chats:
                chats.remove(chat.chat)
            for chat in chats:
                groupmechat = GroupMeChat(chat, False)
                self.chats.append(groupmechat)
                self.need_channels.append(groupmechat)

    def update_groups(self):
        groups = list(self.client.groups.list().autopage())
        if len(groups) != len(self.groups):
            for group in self.groups:
                groups.remove(group.chat)
            for group in groups:
                groupmechat = GroupMeChat(group, True)
                self.groups.append(groupmechat)
                self.need_channels.append(groupmechat)

    def get_msgs(self):
        msgs = {}
        for chat in self.chats:
            msgs.update({chat.channel:chat.get_msgs()})
        for group in self.groups:
            msgs.update({group.channel:group.get_msgs()})
        return msgs

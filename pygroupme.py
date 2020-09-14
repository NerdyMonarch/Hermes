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
        self.webhook = None
        self.last_msg = None

    def get_msgs(self):
        msgs = list(self.chat.messages.list(since_id=self.last_msg))
        if len(msgs) > 0:
            self.last_msg = msgs[0].id
            msgs = msgs[::-1]
        return msgs
    
    def send_msg(self, msg):
        self.chat.post(text=msg)

class PyGroupMe:
    def __init__(self, token):
        self.token = token
        self.client = Client.from_token(token)
        self.user_id = self.client.user.me['user_id']
        self.chats = []
        self.groups = []
        self.need_channels = []
    
    def chat_helper(self, chat):
        for old_chat in self.chats:
            if old_chat.chat.other_user['id'] == chat.other_user['id']:
                return False
        return True
    
    def group_helper(self, group):
        for old_group in self.groups:
            if old_group.chat.id == group.id:
                return False
        return True
    
    def update_chats(self):
        chats = list(self.client.chats.list().autopage())
        if len(chats) > len(self.chats):
            chats = list(filter(self.chat_helper, chats))
            for chat in chats:
                groupmechat = GroupMeChat(chat, False)
                self.chats.append(groupmechat)
                self.need_channels.append(groupmechat)


    def update_groups(self):
        groups = list(self.client.groups.list().autopage())
        if len(groups) > len(self.groups):
            groups = list(filter(self.group_helper, groups))
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
    
    def send_msg(self, channel, msg):
        chats = self.groups + self.chats
        for chat in chats:
            if chat.channel == channel:
                chat.send_msg(msg)
                break

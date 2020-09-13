import discord
import asyncio
import pygroupme

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_listener = self.loop.create_task(self.receiver())

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    
    async def receiver(self):
        await self.wait_until_ready()
        self.server = self.guilds[0]
        self.groupme_category = await self.server.create_category('GroupMe')
        while not self.is_closed():
            self.groupme.update_chats()
            self.groupme.update_groups()
            for chat in self.groupme.need_channels:
                channel = await self.groupme_category.create_text_channel(chat.name)
                chat.channel = channel
                webhook = await channel.create_webhook(name=chat.name)
                chat.webhook = webhook
            self.groupme.need_channels = []
            text_channels = self.groupme_category.text_channels
            msgs = self.groupme.get_msgs()
            for channel in text_channels:
                new_msgs = msgs[channel]
                webhook = await channel.webhooks()
                webhook = webhook[0]
                for msg in new_msgs:
                    if msg.text != None:
                        avatar_url = msg.avatar_url
                        if msg.avatar_url == None:
                            avatar_url = 'https://www.insidehighered.com/sites/default/server_files/styles/large/public/media/GroupMe.jpg?itok=reEAv1vJ'
                        await webhook.send(content=msg.text, username=msg.name, avatar_url=avatar_url)
                    await asyncio.sleep(0.1)
            await asyncio.sleep(1)
    
    async def on_message(self, msg):
        if msg.author != self.user:
            print(msg.content)


class PyCord():
    def __init__(self, token, groupme_token):
        self.token = token
        self.client = DiscordClient()
        self.client.groupme = pygroupme.PyGroupMe(groupme_token)
    
    def run(self):
        self.client.run(self.token)

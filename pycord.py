import discord
import sys

class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print(self.guilds)
    
    async def on_message(self, msg):
        app_info = await self.application_info()
        app_user = app_info.owner
        if msg.author == app_user:
            if msg.content == '!STOP':
                await self.close()
            else:
                print(msg.content)
    
    async def send_msg(self, msg):
        pass


class PyCord():
    def __init__(self, token):
        self.token = token
        self.client = DiscordClient()
    
    def run(self):
        self.client.run(self.token)
    
    def send_msg(self, msg):
        self.client.send_msg(msg)
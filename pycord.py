import discord
import asyncio
import sys

class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.connected = False
        self.running = True

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.connected = True
    
    async def on_message(self, msg):
        app_info = await self.application_info()
        app_user = app_info.owner
        if msg.author == app_user:
            if msg.content == '!STOP':
                self.running = False
                await self.close()
            else:
                print(msg.content)
    
    async def on_connect(self):
        #self.connected = True
        pass
    
    async def create_text_channel(self, name, category):
        guild = self.guilds[0]
        channel = await guild.create_text_channel(name)
        await channel.create_webhook(name=name)
        return channel.id
    
    async def send_msg(self, channel_id, user, msg):
        channel = await self.fetch_channel(channel_id)
        webhook = await channel.webhooks()
        webhook = webhook[0]
        await webhook.send(content=msg, username=user)

class PyCord():
    def __init__(self, token):
        self.token = token
        self.client = DiscordClient()
    
    def run(self):
        self.client.run(self.token)
    
    def create_channel(self, name, category):
        channel = asyncio.run_coroutine_threadsafe(self.client.create_text_channel(name, category),
                                        loop=self.client.loop)
        while not channel.done():
            # Do Nothing
            pass
        channel = channel.result()
        return str(channel)

    def send_msg(self, channel_id, user, msg, avatar):
        asyncio.ensure_future(self.client.send_msg(int(channel_id), user, msg),
                                loop=self.client.loop)
    
    def is_connected(self):
        return self.client.connected

    def is_running(self):
        return self.client.running

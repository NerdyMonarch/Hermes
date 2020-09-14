import os
import pycord
import pygroupme

discord_token = os.environ['DISCORD_TOKEN']
groupme_token = os.environ['GROUP_ME_TOKEN']

cord = pycord.PyCord(discord_token, groupme_token)
cord.run()
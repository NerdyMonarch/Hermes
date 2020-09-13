from dotenv import load_dotenv
import os
import pycord
import pygroupme

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
groupme_token = os.getenv('GROUP_ME_TOKEN')

groupme = pygroupme.PyGroupMe(groupme_token)
cord = pycord.PyCord(discord_token)
cord.run()
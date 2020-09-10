import pycord
import pygroupme
import receiver
from dotenv import load_dotenv
import os

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
group_me_token = os.getenv('GROUP_ME_TOKEN')

groupme = pygroupme.PyGroupMe(group_me_token)
print(groupme.get_msgs())
# pycord = pycord.PyCord(discord_token)
# pycord.run()
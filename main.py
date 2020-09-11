import pycord
import pygroupme
import receiver
import multiprocessing
import threading
from dotenv import load_dotenv
import os

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
group_me_token = os.getenv('GROUP_ME_TOKEN')

pycord = pycord.PyCord(discord_token)
group_me = pygroupme.PyGroupMe(group_me_token)
receiver = receiver.Receiver(pycord, group_me)

process1 = threading.Thread(target=pycord.run)
process2 = threading.Thread(target=receiver.run)

process1.start()
process2.start()

process1.join()
process2.join()
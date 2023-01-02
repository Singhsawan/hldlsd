from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, REPLIT
from time import sleep, time
from psutil import boot_time, disk_usage, net_io_counters
from subprocess import check_output
from os import path as ospath
    
class Bot(Client):

    def __init__(self):
        super().__init__(
        "tg link search bot",
         api_id=API_ID,
         api_hash=API_HASH,
         bot_token=BOT_TOKEN,
         plugins=dict(root="plugins"),
         workers=50,
         sleep_threshold=10
        )

      
    async def start(self):  

        if REPLIT:
            await keep_alive()
            
            
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username

        print('Bot started')


    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

Bot().run()

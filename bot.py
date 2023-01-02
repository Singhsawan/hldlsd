from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, REPLIT
from time import sleep, time
from psutil import boot_time, disk_usage, net_io_counters
from subprocess import check_output
from os import path as ospath
        
            
if REPLIT:
    from flask import Flask, jsonify
    from threading import Thread
    
app = Flask(__name__)
botStartTime = time()
if ospath.exists('.git'):
    commit_date = check_output(["git log -1 --date=format:'%y/%m/%d %H:%M' --pretty=format:'%cd'"], shell=True).decode()
else:
    commit_date = 'No UPSTREAM_REPO'

@app.route('/status', methods=['GET'])
def status():
    bot_uptime = time() - botStartTime
    uptime = time() - boot_time()
    sent = net_io_counters().bytes_sent
    recv = net_io_counters().bytes_recv
    return {
        'commit_date': commit_date,
        'uptime': uptime,
        'on_time': bot_uptime,
        'free_disk': disk_usage('.').free,
        'total_disk': disk_usage('.').total,
        'network': {
            'sent': sent,
            'recv': recv,
        },
    }    
    @app.route('/')
    def main():
        
        res = {
            "status":"running",
            "hosted":"replit.com",
            "repl":REPLIT,
        }
        
        return jsonify(res)

    def run():
      app.run(host="0.0.0.0", port=8000)
    
    async def keep_alive():
      server = Thread(target=run)
      server.start()


class Bot(Client):

    def __init__(self):
        super().__init__(
        "droplink search bot",
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

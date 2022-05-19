import discord
from discord.ext.commands import Bot
import requests
import zipfile
import decrypt
import util
import os
import io
import shutil

def emoticon(url):
    eid, ename = util.getEmoticonInfo(url)
    print("EmoticonId: {}\nEmoticonName: {}".format(eid, ename))

    res = requests.get(util.getEmoticonPackUrl(eid))
    if res.status_code != 200:
        print("{} ERROR".format(res.status_code))
        os.exit(1)
        
    if not os.path.exists(eid):
        os.makedirs(eid)
        
    with zipfile.ZipFile(io.BytesIO(res.content), "r") as zf:
        namelist = zf.namelist()
        for idx, filepath in enumerate(namelist):
            _, ext = os.path.splitext(filepath)

            if util.is_decrypt_required(ext):
                emot = decrypt.xorData(zf.read(filepath))
            else:
                emot = zf.read(filepath)
                
            filename = "{}/{}".format(eid, os.path.basename(filepath))
            
            with open(filename, "wb") as f:
                f.write(emot)
                
            print("success {}/{}".format(idx+1, len(namelist)))

    return eid, ename;

TOKEN = 'OTc2NjMwMjk2Mjk4NTQ1MjAz.Gf_XCb.X75AgxYGlcS3f22GWBEV5N30k5maP1nKk7mIXE'

intents = discord.Intents.default()
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.command()
async def download(ctx, url):
    eid, ename = emoticon(url)
    with zipfile.ZipFile(eid + '.zip', "w") as zf:
        for file in os.listdir(eid):
            zf.write(os.path.join(eid, file))
    file = discord.File(eid + '.zip')
    await ctx.reply('>>> ' + ename, file=file)
    shutil.rmtree(eid)
    os.remove(eid + '.zip')

bot.run(TOKEN)

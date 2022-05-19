import discord
from discord.ext.commands import Bot
import requests
import zipfile
import decrypt
import util
import os
import io
import shutil
from time import sleep


def webp2gif(filename, eid, idx):
    driver.get("https://ezgif.com/maker")
    driver.find_element_by_css_selector("input[type='file']").send_keys(os.path.join(os.getcwd(), filename))
    driver.find_element_by_css_selector("input[type='submit']").click()
    driver.find_element_by_name("nostack").click()
    driver.find_element_by_name("make-a-gif").click()
    while len(driver.find_elements_by_class_name("save")) < 2:
        sleep(1)
    driver.find_elements_by_class_name("save")[1].click()
    while not os.path.isfile("ezgif.com-gif-maker.gif"):
        sleep(1)
    os.rename("ezgif.com-gif-maker.gif", os.path.join(str(eid) + "_gif", str(idx) + ".gif"))


def emoticon_gif(url):
    eid, ename = util.getEmoticonInfo(url)
    print("EmoticonId: {}\nEmoticonName: {}".format(eid, ename))

    res = requests.get(util.getEmoticonPackUrl(eid))
    if res.status_code != 200:
        print("{} ERROR".format(res.status_code))
        os.exit(1)
        
    if not os.path.exists(eid):
        os.makedirs(eid)
        
    if not os.path.exists(eid + "_gif"):
        os.makedirs(eid + "_gif")
        
    with zipfile.ZipFile(io.BytesIO(res.content), "r") as zf:
        namelist = zf.namelist()
        for idx, filepath in enumerate(namelist):
            _, ext = os.path.splitext(filepath)

            if util.is_decrypt_required(ext):
                emot = decrypt.xorData(zf.read(filepath))
            else:
                emot = zf.read(filepath)
                
            filename = "{}/{}".format(eid, os.path.basename(filepath))
            print(filename)
            with open(filename, "wb") as f:
                f.write(emot)
                
            print("success {}/{} WEBP".format(idx+1, len(namelist)))

            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})
            global driver
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

            if os.path.isfile("ezgif.com-gif-maker.gif"):
                os.remove("ezgif.com-gif-maker.gif")

            webp2gif(filename, eid, idx + 1)

            print("success {}/{} GIF".format(idx+1, len(namelist)))
            
    return eid, ename;


def emoticon_webp(url):
    eid, ename = util.getEmoticonInfo(url)
    print("EmoticonId: {}\nEmoticonName: {}".format(eid, ename))

    res = requests.get(util.getEmoticonPackUrl(eid))
    if res.status_code != 200:
        print("{} ERROR".format(res.status_code))
        os.exit(1)
        
    if not os.path.exists(eid):
        os.makedirs(eid)
        
    if not os.path.exists(eid + "_gif"):
        os.makedirs(eid + "_gif")
        
    with zipfile.ZipFile(io.BytesIO(res.content), "r") as zf:
        namelist = zf.namelist()
        for idx, filepath in enumerate(namelist):
            _, ext = os.path.splitext(filepath)

            if util.is_decrypt_required(ext):
                emot = decrypt.xorData(zf.read(filepath))
            else:
                emot = zf.read(filepath)
                
            filename = "{}/{}".format(eid, os.path.basename(filepath))
            print(filename)
            with open(filename, "wb") as f:
                f.write(emot)
                
            print("success {}/{} WEBP".format(idx+1, len(namelist)))
            
    return eid, ename;


TOKEN = os.environ.get('TOKEN')
intents = discord.Intents.default()
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="!readme"))

@bot.command()
async def readme(ctx):
    await ctx.reply("[~10 sec] !WEBP <Emoticon URL>\n[~10 min] !GIF <Emoticon URL>")

@bot.command()
async def gif(ctx, url):
    await ctx.reply("Wait 10 minutes")
    
    eid, ename = emoticon_gif(url)
    
    with zipfile.ZipFile(eid + '.zip', "w") as zf:
        for file in os.listdir(eid):
            zf.write(os.path.join(eid, file))
    with zipfile.ZipFile(eid + '_gif.zip', "w") as zf:
        for file in os.listdir(eid + "_gif"):
            zf.write(os.path.join(eid + "_gif", file))

    file = discord.File(eid + '.zip')
    await ctx.reply('>>> ' + ename + " WEBP", file=file)
    file = discord.File(eid + '_gif.zip')
    await ctx.reply('>>> ' + ename + " GIF", file=file)
    
    shutil.rmtree(eid)
    shutil.rmtree(eid + "_gif")
    os.remove(eid + '.zip')
    os.remove(eid + '_gif.zip')
    
@bot.command()
async def webp(ctx, url):
    eid, ename = emoticon_webp(url)
    
    with zipfile.ZipFile(eid + '.zip', "w") as zf:
        for file in os.listdir(eid):
            zf.write(os.path.join(eid, file))

    file = discord.File(eid + '.zip')
    await ctx.reply('>>> ' + ename + " WEBP", file=file)
    
    shutil.rmtree(eid)
    os.remove(eid + '.zip')

bot.run(TOKEN)

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import pickle
import logging
import ssl
import urllib.parse
import base64
from datetime import datetime,timedelta
from time import sleep
import time
import os
import discord
from dotenv import load_dotenv
import requests
import MySQLdb
from discord.ext.tasks import loop



client = discord.Client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
def _remove_html_tags(html):
    p = re.compile(r'<[^<]*?/?>')
    return p.sub('', html)

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

_opener = urllib2.build_opener()
_opener.addheaders = [('User-agent', 'Mozilla/5.0')]
_events_calendar = {}
_events_list_file = 'events.data'
_url = 'https://www.syracuse.com/'

logging.basicConfig(
    filename='log_histopy.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

html = _opener.open(_url).read()
articles = []
uls = BeautifulSoup(html, "html.parser").html.body.findAll('article')
for x in uls:
  time1 = int(x.attrs['data-publishedon'])
  dt_object = (datetime.fromtimestamp(time1) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
  atetime_object = datetime.strptime(dt_object, '%Y-%m-%d %H:%M:%S')
  if ((atetime_object.hour == (datetime.today()- timedelta(hours=5)).hour) and (atetime_object.day == (datetime.today()- timedelta(hours=5)).day)) :
        articles.append({'header':x.attrs['data-social-hed'],'link':x.attrs['data-source'],'thumb':x.attrs['data-image-thumb'],'publishedOnRaw':int(x.attrs['data-publishedon']), 'id': x.attrs['id']})

#print((datetime.today()- timedelta(hours=5)).day)
if (len(articles) >= 1):
    @loop(count=1)
    async def send_articles():
        channel = client.get_channel(778406469979602954)
        for article in articles:
            publishedOnRaw = article['publishedOnRaw']
            publishedOn = (datetime.fromtimestamp(publishedOnRaw) - timedelta(hours=5))
            embed=discord.Embed(title=article['header'], url=article['link'], description=str(publishedOn))
            embed.set_thumbnail(url=article['thumb'])
            await channel.send(embed=embed)


    @send_articles.before_loop
    async def before_send_articles():
        await client.wait_until_ready()  # Wait until bot is ready.

    @send_articles.after_loop
    async def after_send_articles():
        await client.logout()  # Make the bot log out.

    send_articles.start()
    client.run(TOKEN)

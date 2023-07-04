import asyncio
import json
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from .database import collection
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from translation import *
import urllib.parse
import pymongo
import validate_query

@Client.on_message(filters.private & filters.text & filters.incoming & ~filters.command(['start', 'total']))
async def find_movies(c: Client, m:Message):
   
    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", m.text):
        return
    
    if ("https://" or "http://") in m.text:
        return
    
    query = m.text #
   
    if len(query) < 2:
        return
    query = await validate_query.validate_q(query)

   

    if m.text:

        results = await search_for_videos(query)
        
        list2 = []

        if results:
            for result in results:   
                id = str(result['_id'])
                if m.chat.id in ADMINS:
                    list2 += [
                        InlineKeyboardButton(result['title'], callback_data=f"send#{id}") ,
                        InlineKeyboardButton("Delete", callback_data=f"delete#{id}"),
                        ],
                else:
                    list2 += [InlineKeyboardButton(result['title'], callback_data=f"send#{id}"), ],

            reply_markup=InlineKeyboardMarkup(list2)

            txt = await m.reply(text=f"**Click On Your Movie Name 👇👇 \n And start**", reply_markup=reply_markup)
        
        else:
            google_search_url = "https://www.google.com/search?q=" + escape_url(f"{m.text} Movie")
            release_date_url = "https://www.google.com/search?q=" + escape_url(f"{m.text} Release Date")


            reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Check Correct Spelling ✅", url=google_search_url)],
                [InlineKeyboardButton("Check Realease Date 📅", url=release_date_url)]
            ])

            txt = await m.reply_text(photo="https://graph.org/file/b51582874d65a334073ba.jpg",caption=NO_RESULTS_FOUND.format(m.text, "https://www.google.com/search"), reply_markup=reply_markup)



    # Auto Delete

    if AUTO_DELETE is not False:
        await asyncio.sleep(240)
        await m.delete()
        await txt.delete()


async def search_for_videos(search_text):

    # return collection.find({"$text": {"$search": search_text}}).limit(RESULTS_COUNT)
    # query = collection.find( {"title":search_text}).limit(RESULTS_COUNT)


    x = f"\"{search_text}\""
    pipeline= {
            '$text':{'$search': x }
        }
        
        
    db_list = collection.find(
            pipeline, 
            {'score': {'$meta':'textScore'}}
        ).limit(RESULTS_COUNT)


    query = db_list.sort([("score", {'$meta': 'textScore'})])  # Sort all document on the basics of 


    if query.count() > 0:
        return query


def escape_url(str):
    escape_url = urllib.parse.quote(str)
    return escape_url


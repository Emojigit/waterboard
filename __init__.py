# -*- coding: utf-8 -*-

__author__ = "Emoji"
__version__ = "1.0.0"
__url__ = "https://github.com/Emojigit/waterboard"
__description__ = "Water (so called \"spamming\") leaderboard"
__dname__ = "waterboard"

from telethon import events, utils
from asyncio import sleep
from time import time
numbers = ["🥇 1st","🥈 2nd","🥉 3rd","🏅 4th"] + [str(x) + "th" for x in range(5,10)]
def setup(bot,storage):
    @bot.on(events.NewMessage())
    async def waterboard_count(event):
        if event.is_private: return
        chatid = event.chat_id
        text = event.message.text
        sender = event.sender
        storage_key = "waters_{}".format(chatid)
        if text[0] == "/":
            return # Ignore commands
        waters = storage.get(storage_key,{})
        waters[sender.id] = (waters[sender.id] if sender.id in waters else 0) + 1
        storage.set(storage_key,waters)
    # sorted(a.items(), key=lambda x: int(x[1]))
    @bot.on(events.NewMessage(pattern="/waterboard"))
    async def waterboard(event):
        if event.is_private:
            await event.respond("此指令只在群組有效。")
            raise events.StopPropagation
        returns = []
        returns.append("水群龍虎榜：")
        chatid = event.chat_id
        text = event.message.text
        sender = event.sender
        storage_key = "waters_{}".format(chatid)
        waters = storage.get(storage_key,{})
        if len(waters) == 0:
            returns.append("無資料。")
        else:
            waters_sorted = (sorted(waters.items(), key = lambda x: x[1] * -1))
            place = 0
            for x,y in waters_sorted:
                try:
                    usero = await bot.get_entity(int(x))
                    user = utils.get_display_name(usero)
                except ValueError:
                    user = x
                try:
                    returns.append("{}: [{}](tg://user?id={})，水了 {} 次".format(numbers[place],user,x,y))
                except IndexError:
                    break
                place += 1
        returns.append("運行指令 /waterboard 獲取最新水群資訊！")
        await event.respond("\n".join(returns))
        raise events.StopPropagation


# 🥇🥈🥉🏅

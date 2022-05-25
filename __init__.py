# -*- coding: utf-8 -*-

__author__ = "Emoji"
__version__ = "1.0.0"
__url__ = "https://github.com/Emojigit/waterboard"
__description__ = "Water (so called \"spamming\") leaderboard"
__dname__ = "waterboard"

from telethon import events, utils
from asyncio import sleep
from time import time
bandages_ = {
    15:  ("💧","水滴"),
    30:  ("💦","潑水"),
    50:  ("🚿","花灑"),
    75:  ("🌧","雨水"),
    120: ("🌊","海嘯"),
}
bandages = {x:bandages_[x] for x in reversed(bandages_)}
def get_bandage(waters,short=False):
    for x in bandages.keys():
        if waters >= x:
            y = bandages[x]
            if short:
                return y[0]
            return y[0] + y[1]
    return None
numbers = ["🥇 1st","🥈 2nd","🥉 3rd","🏅 4th"] + [str(x) + "th" for x in range(5,10)]
def setup(bot,storage):
    @bot.on(events.NewMessage())
    async def waterboard_count(event):
        if event.is_private: return
        chatid = event.chat_id
        text = event.message.text
        sender = event.sender
        sender_id = str(sender.id)
        storage_key = "waters_{}".format(chatid)
        if text[0] == "/":
            return # Ignore commands
        waters = storage.get(storage_key,{})
        waters[sender_id] = (waters[sender_id] if sender_id in waters else 0) + 1
        storage.set(storage_key,waters)
    # sorted(a.items(), key=lambda x: int(x[1]))
    @bot.on(events.NewMessage(pattern="/waterboard"))
    async def waterboard(event):
        if event.is_private:
            await event.respond("此指令只在群組有效。")
            raise events.StopPropagation
        async with bot.action(event.chat, 'typing') as action:
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
                waters_sorted = sorted(waters.items(), key = lambda x: int(x[1]) * -1)
                all_waters = 0
                place = 0
                for x,y in waters_sorted:
                    try:
                        usero = await bot.get_entity(int(x))
                        user = utils.get_display_name(usero)
                    except ValueError:
                        user = x
                    band = get_bandage(y,short=True)
                    if band == None:
                        band = ""
                    try:
                        if "noping" in text:
                            returns.append("{}: {}{}，水了 {} 次".format(numbers[place],user,band,y))
                        else:
                            returns.append("{}: [{}](tg://user?id={}){}，水了 {} 次".format(numbers[place],user,x,band,y))
                    except IndexError:
                        pass
                    all_waters += y
                    place += 1
                returns.append("{} 位群員參與了水群。".format(len(waters)))
                returns.append("本群含水量爲 {}，平均每位有參與水群的羣員水了 {} 次。".format(all_waters,round(float(all_waters)/float(len(waters)),1)))
            returns.append("運行指令 /waterboard 獲取最新水群資訊！")
            returns.append("運行指令 /selfwater 獲取自己的水群資訊！")
            returns.append("運行指令 /water [提及或用戶ID] 獲取他人的水群資訊（也可回覆別人省略參數）！")
        await event.respond("\n".join(returns),silent=True)
        raise events.StopPropagation
    @bot.on(events.NewMessage(pattern="/selfwater"))
    async def selfwater(event):
        if event.is_private:
            await event.respond("此指令只在群組有效。")
            raise events.StopPropagation
        async with bot.action(event.chat, 'typing') as action:
            chatid = event.chat_id
            text = event.message.text
            sender = event.sender
            storage_key = "waters_{}".format(chatid)
            waters = storage.get(storage_key,{})
            waters_sorted = sorted(waters.items(), key = lambda x: int(x[1]) * -1)
            for n in range(0,len(waters_sorted)):
                if int(waters_sorted[n][0]) == sender.id:
                    band = get_bandage(waters_sorted[n][1],short=False)
                    if band == None:
                        band = "無勳章"
                    else:
                        band = "勳章爲" + band
                    await event.respond("[你](tg://user?id={})水了 {} 條信息，群內第 {} 名，{}。".format(sender.id,waters_sorted[n][1],n + 1,band))
                    raise events.StopPropagation
            await event.respond("[你](tg://user?id={})沒有水過任何信息。".format(sender.id))
            raise events.StopPropagation
    @bot.on(events.NewMessage(pattern="/water"))
    async def water(event):
        if event.is_private:
            await event.respond("此指令只在群組有效。")
            raise events.StopPropagation
        async with bot.action(event.chat, 'typing') as action:
            chatid = event.chat_id
            text = event.message.text
            sender = event.sender
            try:
                text = text.split(" ",1)[1]
            except IndexError:
                text = ""
            if text.replace(" ","") != "":
                try:
                    text = int(text)
                except ValueError:
                    if text[0] == "@":
                        text = text[1:]
                try:
                    target = await bot.get_input_entity(text)
                except (ValueError,TypeError):
                    await event.respond("找不到用戶。格式：/water [提及或用戶ID，也可回覆代替]")
                    raise events.StopPropagation
            else:
                rep = await event.get_reply_message()
                if rep != None:
                    target = rep.sender
                else:
                    await event.respond("找不到用戶。格式：/water [提及或用戶ID，也可回覆代替]")
                    raise events.StopPropagation
            storage_key = "waters_{}".format(chatid)
            waters = storage.get(storage_key,{})
            waters_sorted = sorted(waters.items(), key = lambda x: int(x[1]) * -1)
            try:
                id = target.user_id
            except AttributeError:
                id = target.id
            for n in range(0,len(waters_sorted)):
                if int(waters_sorted[n][0]) == id:
                    band = get_bandage(waters_sorted[n][1],short=False)
                    if band == None:
                        band = "無勳章"
                    else:
                        band = "勳章爲" + band
                    await event.respond("[他](tg://user?id={})水了 {} 條信息，群內第 {} 名，{}。".format(id,waters_sorted[n][1],n + 1,band))
                    raise events.StopPropagation
            await event.respond("[他](tg://user?id={})沒有水過任何信息。".format(id))
            raise events.StopPropagation


# 🥇🥈🥉🏅

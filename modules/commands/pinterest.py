from telebot.types import InputMediaPhoto
from requests import get as SiBogartAySobrangBaho_hindiNaliligo
import random

def sendRequest(msg, bot, search, count=4):
  loading = bot.reply_to(msg, f"⏳ Searching for {search}...")
  respo = SiBogartAySobrangBaho_hindiNaliligo(f"https://api.kenliejugarap.com/pinterestbymarjhun/?search={search}").json()
  if respo['status']:
    if respo['count'] == 0:
      return bot.reply_to(msg,"[ ERROR ] no image found.")
    if count > 10:
      return bot.reply_to(msg,"[ ERROR ] maximum length to send is 10.")
    urls = random.sample(respo['data'], respo['count'])[:count]
    images = [InputMediaPhoto(url) for url in urls]
    images[0].caption = f"<b>Search:</b> {search}\n<b>Count:</b> {count}\n<i>- by {msg.from_user.first_name}</i>"
    images[0].parse_mode = 'HTML'
    bot.delete_message(loading.chat.id, loading.message_id)
    return bot.send_media_group(msg.chat.id,images)
  else:
    return bot.reply_to(msg, f"[ ERROR ] {respo['response']}")

def pinterest(msg, bot, i):
  args = [l.strip() for l in i.text.split('|')]
  try:
    if len(args) == 1:
      sendRequest(msg, bot, args[0])
    elif len(args) == 2:
      if int(args[1]) > 0:
        count_=int(args[1])
        if count_<1 or count_>10:
          return bot.reply_to(msg, '[ ERROR ] Invalid image count\nminimum 1, maximum 10.')
        search_=args[0]
        if search_:
          sendRequest(msg, bot, search_, count=count_)
        else:
          return bot.reply_to(msg, "[ ERROR ] Imvalid input.")
      else:
        return bot.reply_to(msg, "[ ERROR ] the image count is not valid")
    elif len(args) > 2:
      return bot.reply_to(msg,"[ ERROR ] Invalid format, type '/help pinterest' to see the usage.")
    else:
      return bot.reply_to(msg, "[ ERROR ] Invalid format, type '/help pinterest' to see the usage.")
  except Exception as e:
    print(i.log('error', e))
    bot.reply_to(msg, f"[ ERROR ] {e}")

config = {
  "name": 'pinterest',
  "credits": 'Greegmon',
  "usage": '/pinterest <search> | <count>',
  "description": 'Search image from pinterest',
  "def": pinterest
}
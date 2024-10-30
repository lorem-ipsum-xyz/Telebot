def start(msg, bot, i):
  if msg.chat.type == 'privade':
    return bot.send_message(msg.chat.id,f"Thank you {msg.from_user.first_name} for using GeegaBOT, type '/help' to see my commands.")
  bot.send_message(msg.chat.id, "The bot has started.")

config = {
  "name": 'start',
  "credits": 'Greegmon',
  "desceiption": 'Start the bot',
  "def": start
}
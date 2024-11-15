def start(msg, bot, i):
  bot.send_message(msg.chat.id, f"User ID: <b><code>{msg.from_user.id}</code></b>\nChat ID: <b><code>{msg.chat.id}</code></b>", parse_mode='HTML')

config = {
  "name": 'start',
  "credits": 'Greegmon',
  "desceiption": 'Start the bot',
  "def": start
}
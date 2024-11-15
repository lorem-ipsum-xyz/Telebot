from time import time
from main import online
def online_bot(msg, bot, i):
  message = "<b>BOT ONLINE</b>\n\n"
  for name,val in online.getAll().items():
    uptime = int(f"{time() - val['start_time']:.0f}")
    h,m,s = uptime//3600, (uptime%3600) // 60, uptime%60
    message += f"╭ <b>@{name}</b> <i>({val['id']})</i>\n"
    message += f"╰ <b>{h}</b>h <b>{m}</b>m <b>{s}</b>s\n"
  bot.send_message(msg.chat.id, message, parse_mode='HTML')

config = {
  "name": 'online',
  "credits": 'Greegmon',
  "usage": '/online',
  "botDaddy": True,
  "def": online_bot,
  "description": 'Get all online bots'
}
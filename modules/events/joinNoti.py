def joinNoti(msg, bot, i):
  bot.send_message(msg.chat.id, "New Member+")

config = {
  "name": 'joinoti',
  "credits": joinNoti,
  "event_type": 'new_chat_members',
  "description": 'Someone join the chat'
}
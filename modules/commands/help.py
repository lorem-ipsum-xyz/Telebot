from main import cmd

def help(msg, bot, i):
  args = i.text
  if not args:
    text = ''
    for g in i.bot['commands']:
      stat, val = cmd.get(g)
      if stat == 'success':
        text += f"/{val['name']} - {val['description']}\n"
    bot.send_message(msg.chat.id, text)
  else:
    n,m = cmd.get(args)
    if any(v.isspace() for v in args) or n == 'error':
      return bot.reply_to(msg, "❌ error while getting the command, type '/help help' to see the usage.")
    TEXT = ''
    TEXT += f"Command: {m['name']}\n"
    TEXT += f"Credits: {m['credits']}\n"
    TEXT += f"Usage: {m['usage']}\n"
    TEXT += f"Description: {m['description']}"
    bot.send_message(msg.chat.id, TEXT)
    

config = {
  "name": 'help',
  "credits": 'Christopher',
  "usage": '/help <None>|<cmdName>',
  "description": 'See bot commands',
  #"def": help
}
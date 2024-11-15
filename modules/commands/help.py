from main import cmd

def scape(text):
  special_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
  for char in special_characters:
    text = text.replace(char, f'\\{char}')
  return text

def help(msg, bot, i):
  try:
    args = i.text
    if not args:
      text = ''
      for g in i.bot['commands']:
        stat, val = cmd.get(g)
        if stat == 'success':
          text += f"/{val['name']} - {val['description']}\n"
      bot.send_message(msg.chat.id, text)
    else:
      status,m = cmd.get(args)
      if any(v.isspace() for v in args) or status == 'error':
        return bot.reply_to(msg, "[ ERROR ] while getting the command, type '/help help' to see the usage.")
      name = scape(m['name'])
      credits = scape(m['credits'])
      usage = scape(m['usage'])
      desc = scape(m['description'])
      TEXT = (
        f"*Command*: {name}\n"
        f"*Credits*: {credits}\n"
        f"*Usage*: {usage}\n"
        f"*Description*: {desc}"
      )
      bot.send_message(msg.chat.id, TEXT, parse_mode='MarkdownV2')
  except Exception as e:
    print(i.log('error', e))

config = {
  "name": 'help',
  "credits": 'Christopher',
  "usage": '/help <none>|<cmdName>',
  "description": 'See bot commands',
  "def": help
}
'''
================[ Telegram BOT ]==================
DEV: Christopher
Github: https://github.com/lorem-ipsum-xyz
Facebook: httpa://facebook.com/greegmon.1

- this code is open source, feel free to modify
  this, and if you have a question to developer you
  can dm me on messenger
- Sorry if you can't understand my code :(
==================================================
'''
import os
import importlib
import threading
import telebot
import time
import requests
from box import Box
from tb import Commands, font, Events
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

event = Events()
cmd = Commands()
start = time.time()
load_dotenv()
app = Flask(__name__)

botDaddy = [7207775263]
ACTIVE_BOTS = {
  "GeegaBOT": {
    "name": 'GeegaBOT',
    "id": 7207775263,
    "start_time": start,
    "profile": 'https://api.telegram.org/file/bot7207775263:AAFXZg9q_seXBAr5OHo3v0H2Y4dSwAMUSZM/photos/file_0.jpg',
    "token": '7207775263:AAFXZg9q_seXBAr5OHo3v0H2Y4dSwAMUSZM',
    "commands": ['help','start','uptime'],
    "api": telebot.TeleBot('7207775263:AAFXZg9q_seXBAr5OHo3v0H2Y4dSwAMUSZM',parse_mode=None),
    "owner": {
      "name": 'Greegmon',
      "id": 7075537944,
      "links": [
        ('facebook', 'https://facebook.com/greegmon.1'),
        ('github', 'https://github.com/Greegmon')
      ]
    }
  }
}

class CreateBot:
  def __init__(self, token, commands, owner_name='Anonymous', owner_id=1234567890, owner_links=[]):
    self.name = 'BilatBot'
    self.id = None
    self.profile = 'https://i.ibb.co/C73dv1F/default.jpg' # Default image
    self.token = token
    self.start_time = time.time()
    self.commands = commands
    self.api = telebot.TeleBot(token, parse_mode=None)
    self.owner_name = owner_name
    self.owner_id = owner_id
    self.owner_links = owner_links
    
    self.baseUrl = 'https://api.telegram.org'
    if not self.isValidToken():
      raise ValueError('Invalid bot token')
  def create(self):
    ACTIVE_BOTS[self.name] = {
      "name": self.name,
      "id": self.id,
      "token": self.token,
      "start_time": self.start_time,
      "profile": self.profile,
      "commands": self.commands,
      "api": self.api,
      "owner": {
        "name": self.owner_name,
        "id": self.owner_id,
        "links": self.owner_links
      }
    }
    self.registerCommand(self.commands)
    return {
      "name":self.name,
      "id":self.id,
      "profile": self.profile,
      "commands":self.commands,
      "owner": {
        "name": self.owner_name,
        "id": self.owner_id,
        "links": self.owner_links
      }
    }
  def isValidToken(self):
    res = requests.get(f"{self.baseUrl}/bot{self.token}/getMe")
    if res.status_code == 200:
      data = res.json()['result']
      self.name = data['username']
      self.id = data['id']
      self.profile = self.getProfile(self.token, data['id']) or self.profile
      return True
    return False
  def getProfile(self,token,id):
    pfp = f"{self.baseUrl}/file/bot{token}/photos/file_0.jpg"
    response = requests.get(pfp)
    if response.status_code == 200:
      imgbbKey = os.getenv("IMGBB_KEY")
      res = requests.post(f'https://api.imgbb.com/1/upload?key={imgbbKey}', data={"image": pfp, "name": self.name})
      if res.ok:
        return res.json()['data']['url']
    return None
  def registerCommand(self, commands):
    CMDS = list()
    for IK in commands:
      _s,val = cmd.get(IK)
      if _s == 'success':
        CMDS.append(telebot.types.BotCommand(val['name'], val['description']))
    self.api.set_my_commands(CMDS)

# =========================================
@app.route('/home')
@app.route('/')
def root():
  return render_template('home.html'), 200

@app.route('/tuts/<page>')
def tutorial(page):
  if page in ['get_bot_token','get_my_id','create_bot']:
    return render_template('tutorial.html', title=page),200
  return render_template('404.html')

@app.route('/getCommands', methods=['GET'])
def get_commands():
  kupal = list()
  for key, value in cmd.get_all().items():
    if value.get('forDaddy'):
      pass
    else:
      kupal.append(key)
  return jsonify(kupal),200

@app.route('/actives',methods=['GET'])
def active_bot():
  active = []
  for name, val in ACTIVE_BOTS.items():
    active.append({
      "name": name,
      "id": val['id'],
      "profile": val['profile']
    })
  return jsonify(active),200

@app.route('/login', methods=['POST'])
def login():
  try:
    data = request.json
    TOKEN = data.get('token')
    COMMANDS = data.get('commands')
    OWNER_NAME = data.get('owner_name')
    OWNER_ID = data.get('owner_id')
    OWNER_LINKS = data.get('owner_links')
    
    # Create the bot
    BOT = CreateBot(TOKEN, COMMANDS, owner_name=OWNER_NAME, owner_id=OWNER_ID, owner_links=OWNER_LINKS)
    tae = BOT.create()
    data = {
      "name": tae['name'],
      "commands": tae['commands'],
      "id": tae['id'],
      "owner": tae['owner']
    }
    return jsonify(tae),200
  except ValueError as e:
    return jsonify({"status": 'error', "message": str(e)}),403

def start_flask():
  app.run()
# =========================================

def register_command(bot, name, func, info):
  f=info['commands']
  if name.lower() in f:
    @bot.message_handler(commands=[name.lower(), name.upper(), name.title()])
    def handle_command(msg):
      text = msg.text.split(' ', 1)
      obj = Box({
        'font': font,
        'cmd': text[0],
        'text': text[1] if len(text) > 1 else None,
        'bot': {
          "name": info["name"],
          "id": info["id"],
          "start_time": info['start_time'],
          "token": info["token"],
          "profile": info["profile"],
          "commands": info["commands"],
          "owner": info['owner']
        }
      })
      func(msg, bot, obj)
alreadyLoad = False
def reg_cmd(bot,_):
  global alreadyLoad
  xil=list(filter(lambda file: file.endswith('.py') and file!='__init__.py',os.listdir('./modules/commands')))
  zil=list(filter(lambda file: file.endswith('.py') and file!='__init__.py',os.listdir('./modules/events')))
  
  for file in xil:
    filepath = f'modules.commands.{os.path.splitext(file)[0]}'
    module = importlib.import_module(filepath)
    config = getattr(module, 'config', None)
    if config:
      name, func = config.get('name'), config.get('def')
      if name and func:
        cName = name.strip()
        if any(s.isspace() for s in cName):
          if not alreadyLoad:
            print(f"\033[0;91m[ ERROR ] \033[36m({file}) \033[0mCommand name should not include spaces")
        else:
          if not alreadyLoad:
            getCmd = cmd.get(name)
            if getCmd[0] == 'error':
              print(f"\033[0;93m[ COMMAND ] Loaded \033[1;93m{cName} - \033[0;36m({file})")
              config['filename'] = file
              cmd.add(config)
            else:
              print(f"\033[0;91m[ WARNING ] \033[97m([\033[33m{cName}]\033[97m]|\033[36m{o[1]["filename"]}\033[97m) - Duplication command name")
          else:
            register_command(bot, cName, func, _)
      else:
        if not alreadyLoad:
          print(f"\033[0;91m[ ERROR ] \033[36m({file}) \033[0mMissing 'def' or 'name' key in config.")
  for file in zil:
    fullpath = f"modules.events.{os.path.splitext(file)[0]}"
    module = importlib.import_module(fullpath)
    config = getattr(module,'config',None)
    if config:
      name, event_type, func = (
        config.get('name'),
        config.get('event_type'),
        config.get('def')
      )
      #print(config.get('name'))
  if not alreadyLoad:
    print(f"\033[0;92m[ PING ] \033[0m{(time.time() - start)*1000:.2f}ms")
    alreadyLoad = True

def start_bot(bot,_):
  reg_cmd(bot,_)
  bot.infinity_polling()
#--------------

def monitor():
  processed_bots = set()
  while True:
    for jkl in ACTIVE_BOTS.items():
      cmdName, val = jkl
      if cmdName not in processed_bots:
        h = threading.Thread(target=start_bot, args=(val['api'],val))
        h.start()
        processed_bots.add(cmdName)
    time.sleep(1)

if __name__ == '__main__':
  #app.run(debug=True)
  flsk = threading.Thread(target=start_flask)
  flsk.start()
  
  time.sleep(0.2)
  reg_cmd(None,None)
  
  montr = threading.Thread(target=monitor)
  montr.start()
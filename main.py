'''
---------> [ Telebot (not done yet) ] <----------
  Developer: Greegmon
  Github: https://github.com/Greemon
  Facebook: https://facebook.com/greegmon.1

pyTelegramBotAPI (telebot) documentation:
  -> https://pytba.readthedocs.io

mga kupal sa Chatbot Community: 
  • BOGART (https://www.facebook.com/bogart.magalpok.2024)
  • JUNMAR (https://www.facebook.com/profile.php?id=100081852204977)
  • ASHLEY (https://www.facebook.com/ystellafavoredieu)
  • KENT NATHAN (https://www.facebook.com/profile.php?id=61550088000548)
'''
import os
import importlib
import threading
import time
import requests
import telebot
import telebot.util as Util
from box import Box
from tb import Commands, Online
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from utils import (
  log
)

app = Flask(__name__)
cmd = Commands()
online = Online
load_dotenv()
start = time.time()

botDaddy = [7207775263]
god = [7075537944]

class CreateBot:
  def __init__(self, token, commands, owner_name='Anonymous', owner_id=1234567890, owner_links=[]):
    self.name = 'BilatBot'
    self.id = None
    self.profile = 'https://i.ibb.co/C73dv1F/default.jpg' # Default image
    self.token = token
    self.start_time = time.time()
    self.commands = commands
    self.api = telebot.TeleBot(token, parse_mode='HTML')
    self.owner_name = owner_name
    self.owner_id = owner_id
    self.owner_links = owner_links
    
    self.baseUrl = 'https://api.telegram.org'
    if not self.isValidToken():
      raise ValueError('Invalid bot token')
  def create(self) -> tuple:
    online.new({
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
    })
    self.registerCommand(self.commands)
    return ({
      "name":self.name,
      "id":self.id,
      "profile": self.profile,
      "commands":self.commands,
      "owner": {
        "name": self.owner_name,
        "id": self.owner_id,
        "links": self.owner_links
      }
    }, self.api)
  def isValidToken(self) -> bool:
    res = requests.get(f"{self.baseUrl}/bot{self.token}/getMe")
    if res.status_code == 200:
      data = res.json()['result']
      self.name = data['username']
      self.id = int(data['id'])
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

def isBotAlreadyCreated(token):
  for _,value in online.getAll().items():
    if value['token'] == token:
      return True
  return False

# =========================================
@app.route('/home')
@app.route('/')
def root():
  return render_template('home.html'),200

@app.route('/tuts/<page>')
def tutorial(page):
  return render_template('tutorial.html', title=page)

@app.route('/getCommands', methods=['GET'])
def get_commands():
  kupal = list()
  for key, value in cmd.get_all().items():
    if not value.get('forDaddy'):
      kupal.append(key)
  return jsonify(kupal),200

@app.route('/actives',methods=['GET'])
def active_bot():
  active = []
  for name, val in online.getAll().items():
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
    
    if isBotAlreadyCreated(TOKEN):
      return ({"status": 'error', "message": 'The bot token has already been added to the list.'}),1002
    
    # Create the bot
    BOT = CreateBot(TOKEN, COMMANDS, owner_name=OWNER_NAME, owner_id=OWNER_ID, owner_links=OWNER_LINKS)
    tae = BOT.create()
    data = {
      "name": tae[0]['name'],
      "commands": tae[0]['commands'],
      "id": tae[0]['id'],
      "owner": tae[0]['owner']
    }
    
    return data
  except ValueError as e:
    return jsonify({"status": 'error', "message": str(e)}),1001

@app.route('/logout', methods=['GET'])
def logout():
  token = request.args.get('token')
  for _,val in online.getAll().items():
    if val['token'] == token.strip():
      online.delete(token=token.strip())
      return jsonify({"status": 'success'}),200
  return jsonify({"status": 'error', "message": 'bot token not found in the list, double check if the provided token is valid'}),1002

def start_flask():
  app.run()
# =========================================

def register_command(bot, name, func, info):
  f=info['commands']
  if name.lower() in f:
    @bot.message_handler(commands=[name.lower(), name.upper(), name.title()])
    def handle_command(msg):
      command,arguments = Util.extract_command(msg.text),Util.extract_arguments(msg.text)
      obj = Box({
        'line': '━━━━━━━━━━━━━━━━━━━', # Wala lang to :)
        'cmd': command,
        'text': arguments,
        'log': log,
        'bot': {
          "name": info["name"],
          "id": int(info["id"]),
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
              print(f"\033[0;91m[ WARNING ] \033[97m([\033[33m{cName}]\033[97m]|\033[36m{o[1]['filename']}\033[97m) - Duplication command name")
          else:
            register_command(bot, cName, func, _)
      else:
        if not alreadyLoad:
          print(f"\033[0;91m[ ERROR ] \033[36m({file}) \033[0mMissing 'def' or 'name' key in config.")
  if not alreadyLoad:
    print(f"\033[0;92m[ PING ] \033[0m{(time.time() - start)*1000:.2f}ms")
    alreadyLoad = True

def start_bot(bot,_):
  reg_cmd(bot,_)
  bot.polling()
#--------------

def monitor():
  processed_bots = set()
  while True:
    for jkl in online.getAll().items():
      cmdName, val = jkl
      if cmdName not in processed_bots:
        h = threading.Thread(target=start_bot, args=(val['api'],val))
        h.start()
        processed_bots.add(cmdName)
    time.sleep(0.5)

if __name__ == '__main__':
  #app.run(debug=True)
  flsk = threading.Thread(target=start_flask)
  flsk.start()
  
  time.sleep(0.2)
  reg_cmd(None,None)
  
  montr = threading.Thread(target=monitor)
  montr.start()

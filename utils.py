import json

database = json.load(open('db/database.json','r'))

def log(tp, message):
  match tp.lower():
    case 'error':
      return f"\033[0m\033[1;91m[ ERROR ]\033[0;31m {message}"
    case _:
      return message
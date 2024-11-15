class Online:
  online = {}
  @classmethod
  def getAll(cls):
    return cls.online
  @classmethod
  def new(cls, obj):
    cls.online[obj['name']] = obj
  @classmethod
  def delete(cls, token=None, name=None):
    for key,value in self.online.items():
      if value['token'] == token or key == name:
        del self.online[key]
        return 'success'
    return 'error'

class Commands:
  commands = {}
  CommandList = []
  @classmethod
  def add(cls, obj):
    name = obj['name'].strip().lower()
    if name not in cls.commands:
      cls.CommandList.append(name)
      cls.commands[name] = {
        'name': name,
        'filename': obj['filename'],
        'forDaddy': obj.get('forDaddy', False),
        'credits': obj.get('credits', 'Christopher') or 'Greegmon',
        'description': obj.get('description', 'No description.') or 'No description.',
        'usage': obj.get('usage', 'No usage.'),
        'def': obj['def']
      }
      
  @classmethod
  def get_all(cls):
    return cls.commands
  
  @classmethod
  def get_list(cls):
    return cls.CommandList
    
  @classmethod
  def get(cls, command_name):
    cmd = command_name.strip().lower()
    if cmd in cls.commands:
      return ('success', cls.commands[cmd])
    else:
      return ('error', f'Command {command_name} not found.')
  
  @classmethod
  def getCommandNames(cls):
    return [cmdName for cmdName,_ in cls.commands.items()]
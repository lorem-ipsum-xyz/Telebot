class Events:
  """
  Here is the lists of event types in Telebot,
  You can also create your own custom event.
  
  - text: text messages sent by users.
  - audio: Audio file sent by users (e.g., mp3).
  - document: Any general file sent (e.g., ZIP, PDF).
  - photos: Photos or Images.
  - sticker: Telegram stickers.
  - videos: Video files (not short video messages)
  - video_note: Video notes (circular video)
  - voice: Voice messages (audi clips)
  - location: Geolocation information.
  - contact: Contact information.
  
  - new_chat_members: Triggered when a new user joins a chat.
  - left_chat_member: Triggered when a user leaves or is removed for tha chat.
  - new_chat_title: Triggered when the chat title changes.
  - new_chat_photo: Triggered when the chat photo changes.
  - delete_chat_photo: Triggered when the chat photo is deleted.
  - pinned_message: When a message is pinned in the chat.
  
  - group_chat_created: Triggered when a group chat is created.
  - supergroup_chat_created: Triggered when a supergroup is created.
  - channel_chat_created: Triggered when a channel is created.
  
  - migrate_to_chat_id: When a group is upgraded to a supergroup.
  - migrate_from_chat_id: When a supergroup is downgraded to a group.
  
  - invoice: invoice sent through Telegram payments.
  - successful_payment: Notification of successful payments.
  - connected_website: When a user logs in via Telegram's web login.
  """
  eventLists = [
    'text', 'audio', 'document', 'photo', 'sticker',
    'video', 'video_note', 'voice', 'location', 'contact',
    'new_chat_members', 'left_chat_member', 'new_chat_title',
    'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 
    'supergroup_chat_created', 'channel_chat_created',
    'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
    'invoice', 'successful_payment', 'connected_website'
  ]
  
  @classmethod
  def getEvents(cls):
    return cls.eventLists

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

def font(type, text):
	bold_map = {
    'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶',
    'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿',
  	's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
    'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜',
    'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥',
    'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭'
	}
	if type == 'bold':
	   return ''.join(bold_map.get(char, char) for char in text)
	return text
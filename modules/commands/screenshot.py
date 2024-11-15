import re 
import requests
import base64
from bs4 import BeautifulSoup
from io import BytesIO

pattern = re.compile(r"https?://[^\s]+")

def function(msg, bot, i):
  if not i.text:
    return bot.send_message(msg.chat.id, f"Please provide a link.\nUsage example: /ss <code>https://github.com/Greegmon</code>", parse_mode='HTML')
  try:
    match = pattern.search(i.text)
    if match:
      header={"User-Agent": 'Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.163 Mobile Safari/537.36'}
      res = requests.get('https://urltoscreenshot.com/',headers=header)
      soup = BeautifulSoup(res.content, 'html.parser')
      m1 = soup.find_all('script')
      m2 = m1.pop().get_text()
      KEY = m2.split("x-api-key', '")[1].split("'")[0]
      url = 'https://api.apilight.com/screenshot/get'
      data = {
      	'url': match.group(),
      	'base64': '1',
      	'width': 1366,
      	'height': 1024
      }
      header['x-api-key'] = KEY
      response = requests.get(url, headers=header, params=data).text
      base64_image = response
      image_data = base64.b64decode(base64_image)
      image = BytesIO(image_data)
      image.name = 'Website.png'
      bot.send_photo(msg.chat.id, image)
    else:
      return bot.send_message(msg.chat.id, f"Please provide a link.\nUsage example: /ss <code>https://github.com/Greegmon</code>",parse_mode='HTML')
  except Exception as e:
    print(i.log('error',e))
    bot.reply_to(msg, f"[ ERROR ] {e}")

config = {
  "name": 'ss',
  "credits": 'Greegmon',
  "usage": f'/ss <link>',
  "description": 'Screenshot website',
  "def": function
}
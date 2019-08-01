import local_settings.py

server = 'irc.chat.twitch.tv'
port = 6667
nickname = os.environ.get('NICKNAME')
token = os.environ.get('TWITCH_TOKEN')
channel = '#biff_waverider'
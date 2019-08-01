from local_settings import NICKNAME, TOKEN, CHANNEL
import socket
import re

server = 'irc.chat.twitch.tv'
port = 6667
nickname = NICKNAME
token = TOKEN
channel = CHANNEL

sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))


while True:
  resp = sock.recv(2048).decode('utf-8')

  if resp.startswith('PING'):
    sock.send("PONG\n".encode('utf-8'))
    print('sent PONG')
  
  # elif resp.startswith(':tmi.twitch.tv'):
  #   print('caught :tmi.twitch.tv')
  

  elif len(resp) > 0:
    print('response:\n', resp)
    # username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp).groups()
    # username, message = re.split('[:]', resp)
    # print(f"Username: {username}\t Message: {message}\n")
    # res = re.split('[:]', resp)
    # print(res)

  resp = None

# sock.close()

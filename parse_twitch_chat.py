# import sys
# sys.path.append('../')
import signal
from local_settings import NICKNAME, TOKEN, CHANNEL
import socket
import re

server = 'irc.chat.twitch.tv'
port = 6667
nickname = NICKNAME
token = TOKEN
channel = "worldofwarships"

sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# Will clean up and close sockets on CTRL-C
def keyboardInterruptHandler(signal, frame):
  print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
  sock.close()
  print("Socket closed\n\n")
  exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

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
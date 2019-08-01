# import sys
# sys.path.append('../')
import signal
from local_settings import NICKNAME, TOKEN, CHANNEL
import socket
import re
import time

server = 'irc.chat.twitch.tv'
# port = 6667
port = 80
nickname = NICKNAME
token = TOKEN
channel = CHANNEL
RAFFLE = False

reg = r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'

sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# Will clean up and close sockets on CTRL+C
def keyboardInterruptHandler(signal, frame):
  print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
  sock.close()
  print("Socket closed\n\n")
  exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)
print("Press <CTRL+C> to end program and close sockets\n")

def parse_message(resp):

  # needed to assign vars to something else it crashes on NoneType
  username = 'none'
  channel = 'none'
  message = 'none'

  res = re.match(reg, resp)
  
  if res:
    username, channel, message = res.groups()
  
  return username, channel, message

  
def check_for_raffle(message):
  if message.startswith('!raffle'):
    return True
  return False

count=0
ticks=0
while True:
  resp = sock.recv(2048).decode('utf-8')
  # print(resp)

  if resp.startswith('PING'):
    sock.send("PONG\n".encode('utf-8'))
    print('sent PONG')
  
  elif resp.startswith(':tmi.twitch.tv'):
    # print('caught: :tmi.twitch.tv')
    continue
  

  elif len(resp) > 0:
    # print('message:\n', resp)
    # username=msg[msg.find(':')+1:msg.find('!')]
    # print(username)
    # privmsg = msg.split(':')
    # print(privmsg)
    # username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', msg).groups()
    # print(re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', msg))
    # res = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', msg)
    # print(res)
    
    # res = re.match(reg, resp)
    # if res:
      
    #   print(res.groups())
    #   username, channel, message = res.groups()
    #   print(f"Username: {username}\t Channel: {channel}\t Message: {message}\n")
    
    username, channel, message = parse_message(resp)
    print(f"Username: {username}\t Channel: {channel}\t Message: {message}\n")

    if check_for_raffle(message):
      if not RAFFLE:
        RAFFLE = True
        time_start = time.time() # in ticks
        count+=1
    
      
      print('raffle message!')
      print(ticks, count)
    
      


    # if (res.group()):
    #   print(res.group())
    # username, message = re.split('[:]', msg)
    # print(f"Username: {username}\t Message: {message}\n")
    # res = re.split('[:]', msg)
    # print(res)
    # print(sock.getpeername())
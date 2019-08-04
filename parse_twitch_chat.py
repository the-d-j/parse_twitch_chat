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

RAFFLE = False   # is a raffle occurring now?
ENTERED_RAFFLE = False  # have I entered the raffle?
START_TIME = 0   # start time of raffle detection
CURRENT_TIME = 0 # used to determine elapsed time of raffle
COUNT = 0  # Number of raffle entries - used to verify raffle is actually occurring (mitigate false starts)

# pattern to match for username, channel, message
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
    username, channel, message = parse_message(resp)
    print(f"Username: {username}\t Channel: {channel}\t Message: {message}\n")

    # Raffle word detected?
    if check_for_raffle(message):
      if ENTERED_RAFFLE:
        elapsed_time = CURRENT_TIME - START_TIME
        if elapsed_time > 900: # 15min
          RAFFLE = False
          ENTERED_RAFFLE = False
          COUNT = 0
      
      elif not RAFFLE:
        RAFFLE = True
        START_TIME = time.time() 
        COUNT+=1
      
      else:
        CURRENT_TIME = time.time()
        COUNT+=1
        elapsed_time = CURRENT_TIME - START_TIME
        # if (COUNT > 40) and (elapsed_time > 40):
        if (COUNT > 10) and (elapsed_time > 15):
          # Send message works!
          sock.send("PRIVMSG #biff_waverider :!raffle\n".encode('utf-8'))
          print("Raffle entered!")
          ENTERED_RAFFLE = True 
    

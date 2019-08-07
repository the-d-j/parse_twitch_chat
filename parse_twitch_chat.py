import signal
from local_settings import NICKNAME, TOKEN, CHANNEL
import socket
import re
import time
import random

server = 'irc.chat.twitch.tv'
# port = 6667
port = 80

# RAFFLE = False   # is a raffle occurring now?
# ENTERED_RAFFLE = False  # have I entered the raffle?
# ENTERED_RAFFLE_TIME = 0
# START_TIME = 0   # start time of raffle detection
# CURRENT_TIME = 0 # used to determine elapsed time of raffle
# COUNT = 0  # Number of raffle entries - used to verify raffle is actually occurring (mitigate false starts)
# SECOND_ENTRY = False # Re-enter raffle after 30secs to ensure valid entry
# RESPONSES = ["hey!", "yes!", "cool!", "bam!", "thanks!" "woohoo!", "ah yeah", "noice!", "sweet", "yup yup"]

# Will clean up and close sockets on CTRL+C
def keyboardInterruptHandler(signal, frame):
  print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
  sock.close()
  print("Socket closed\n\n")
  exit(0)

def parse_message(resp):
  # needed to assign vars to some value else it crashes on NoneType b/c send.sock() blocking
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

def check_for_winner(username, message, channel, nickname, responses):
  if (username == "nightbot") and (message.startswith(nickname + " has won the giveaway")):
  # if (username == "bella_smurf") and (message.startswith(nickname + " has won the giveaway")):
    time.sleep(4)
    msg = "PRIVMSG "+channel+" :"+responses[random.randrange(len(responses))]+"\n"    
    sock.send(msg.encode('utf-8'))
    time.sleep(5)
    msg = "PRIVMSG "+channel+" :"+responses[random.randrange(len(responses))]+"\n"
    sock.send(msg.encode('utf-8'))
    time.sleep(5)
    msg = "PRIVMSG "+channel+" :"+responses[random.randrange(len(responses))]+"\n"    
    sock.send(msg.encode('utf-8'))
    print("*** Giveaway won! ***\t{}".format(time.ctime()))


#################################################################################################
def main():

  RAFFLE = False   # is a raffle occurring now?
  ENTERED_RAFFLE = False  # have I entered the raffle?
  ENTERED_RAFFLE_TIME = 0
  START_TIME = 0   # start time of raffle detection
  CURRENT_TIME = 0 # used to determine elapsed time of raffle
  COUNT = 0  # Number of raffle entries - used to verify raffle is actually occurring (mitigate false starts)
  SECOND_ENTRY = False # Re-enter raffle after 30secs to ensure valid entry
  RESPONSES = ["hey!", "yes!", "cool!", "bam!", "thanks!" "woohoo!", "ah yeah", "noice!", "sweet", "yup yup"]

  # TODO: Log wins / Send alert message?
  # Future version: Rewrite into OO to support different channel raffles
  while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
      sock.send("PONG\n".encode('utf-8'))
      # print('sent PONG')
    
    elif resp.startswith(':tmi.twitch.tv'):
      # print('caught: :tmi.twitch.tv')
      continue

    elif len(resp) > 0:
      username, channel, message = parse_message(resp)
      # print(f"Username: {username}\t Channel: {channel}\t Message: {message}\n")

      check_for_winner(username, message, CHANNEL, NICKNAME, RESPONSES)

      # Raffle word detected?
      if check_for_raffle(message):
        if not RAFFLE:
          RAFFLE = True
          START_TIME = time.time() 
          COUNT+=1
        else:
          CURRENT_TIME = time.time()
          COUNT+=1
          elapsed_time = CURRENT_TIME - START_TIME
          
          if (COUNT > 40) and (elapsed_time > 80) and not ENTERED_RAFFLE:
          # if (COUNT > 10) and (elapsed_time > 30) and not ENTERED_RAFFLE: # Test values
            # Send message works! Needs: PRIVMSG #<channel> :<msg>
            msg = "PRIVMSG "+CHANNEL+" :!raffle\n"
            sock.send(msg.encode('utf-8'))
            print("* Raffle entered! *\n")
            ENTERED_RAFFLE = True 
            ENTERED_RAFFLE_TIME = time.time()
            print(time.ctime(ENTERED_RAFFLE_TIME))
      
    # Due to socket being blocking this will only work when a msg is received
    if ENTERED_RAFFLE:
      curr_time = time.time()
      elapsed_time = curr_time - ENTERED_RAFFLE_TIME

      # Has it been 15min since the raffle began?
      # If so, reset for next raffle
      if elapsed_time > 900: # 15min
        RAFFLE = False
        ENTERED_RAFFLE = False
        ENTERED_RAFFLE_TIME = None
        START_TIME = None
        CURRENT_TIME = None
        COUNT = 0
        print("Settings reset; raffle over (or timed out)\n\n")

    # print("Statuses:\nRAFFLE:  {}\nENTERED_RAFFLE:  {}\nENTERED_RAFFLE_TIME:  {}\nSTART_TIME:  {}\nCURRENT_TIME:  {}\nCOUNT:  {}\n"
      # .format(RAFFLE, ENTERED_RAFFLE, time.ctime(ENTERED_RAFFLE_TIME), time.ctime(START_TIME), time.ctime(CURRENT_TIME), COUNT))

  """ Causing inappropriate timing which looks bot-ish? """
      # # Re-enter to ensure valid entry
      # elif (elapsed_time > 35) and not SECOND_ENTRY:
      #   msg = "PRIVMSG "+CHANNEL+" :!raffle\n"
      #   sock.send(msg.encode('utf-8'))
      #   SECOND_ENTRY = True
      #   print("Second Raffle entry!")
### END MAIN() ###



# pattern to match for username, channel, message
reg = r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'

sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {TOKEN}\n".encode('utf-8'))
sock.send(f"NICK {NICKNAME}\n".encode('utf-8'))
sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))

signal.signal(signal.SIGINT, keyboardInterruptHandler)
print("Press <CTRL+C> to end program and close sockets\n")

main()

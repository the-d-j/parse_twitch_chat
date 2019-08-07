import signal
import socket
import re
import time
import random
import local_settings

 # Will clean up and close sockets on CTRL+C
def keyboardInterruptHandler(self, signal, frame):
  print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
  # self.sock.close()
  print("Socket closed\n\n")
  exit(0)


class Bot:

  def __init__(self, token, nickname, channel, server='irc.chat.twitch.tv', port=80):
    self.token = token
    self.nickname = nickname
    self.channel = channel
    self.server = server
    self.port = port

    self.raffle_started = False
    self.entered_raffle = False
    self.entered_raffle_time = 0
    self.raffle_start_time = 0
    self.current_time = 0
    self.elapsed_time = 0
    self.count = 0
    self.responses = ["hey!", "yes!", "cool!", "bam!", "thanks!" "woohoo!", "ah yeah", "noice!", "sweet", "yup yup"]
  
    self.sock = socket.socket()
    self.sock.connect((self.server, self.port))

    self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
    self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
    self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))

    
  ### END INIT ###
  
  def status(self):
    print("Statuses for channel {}:\nRAFFLE_STARTED:  {}\nENTERED_RAFFLE:  {}\nENTERED_RAFFLE_TIME:  {}\nRAFFLE_START_TIME:  {}\nCURRENT_TIME:  {}\nCOUNT:  {}\n"
      .format(self.channel, self.raffle_started, self.entered_raffle, time.ctime(self.entered_raffle_time),
      time.ctime(self.raffle_start_time), time.ctime(self.current_time), self.count))
    return

  def parse_message(self, resp):
    # regex pattern to match for username, channel, message
    reg = r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'

    # needed to assign vars to some value else it crashes on NoneType b/c send.sock() blocking...
    username = 'none'
    channel = 'none'
    message = 'none'

    res = re.match(reg, resp)
    if res:
      username, channel, message = res.groups()
    return username, channel, message

  def check_for_winner(self, username, message):
    if (username == 'nightbot') and (messasge.startswith(self.nickname + " has won the giveaway")):
      time.sleep(4)
      msg = "PRIVMSG " + self.channel + " :" + self.responses[random.randrange(len(self.responses))]+"\n"
      self.sock.send(msg.encode('utf-8'))
      time.sleep(5)
      msg = "PRIVMSG " + self.channel + " :" + self.responses[random.randrange(len(self.responses))]+"\n"
      self.sock.send(msg.encode('utf-8'))
      time.sleep(5)
      msg = "PRIVMSG " + self.channel + " :" + self.responses[random.randrange(len(self.responses))]+"\n"
      self.sock.send(msg.encode('utf-8'))
      print('*** GIVEAWAY WON! ***\t{}'.format(time.ctime()))
    return

  def check_for_raffle(self, message):
    if message.startswith('!raffle'):
      if not self.raffle_started:
        self.raffle_started = True
        self.raffle_start_time = time.time()
        self.count = self.count + 1
      else:
        print("in check_for_raffle\n\n")

        self.current_time = time.time()
        self.count = self.count + 1
        self.elapsed_time = self.current_time - self.raffle_start_time
    return

  def enter_raffle(self):
    msg = "PRIVMSG " + self.channel + " :!raffle\n"
    self.sock.send(msg.encode('utf-8'))
    self.entered_raffle = True
    self.entered_raffle_time = time.time()
    print("* Raffle entered! *\t{}".format(time.ctime(self.entered_raffle_time)))
    return

  def reset(self):
    self.raffle_started = False
    self.raffle_start_time = 0
    self.entered_raffle = False
    self.entered_raffle_time = 0
    self.current_time = 0
    self.count = 0
    print("Settings reset; raffle over (or timed out)\n\n")
    return

### END class Bot ###

# TODO: Check for winner
# TODO: Incorporate json for multiple giveaways
def main():
  signal.signal(signal.SIGINT, keyboardInterruptHandler)
  print("Press <CTRL+C> to end program and close sockets\n")

  obj = Bot(local_settings.TOKEN, local_settings.NICKNAME, local_settings.CHANNEL)
  while True:
    resp = obj.sock.recv(2048).decode('utf-8')
    if resp.startswith('PING'):
      obj.sock.send("PONG\n".encode('utf-8'))
      print("send PONG")
    
    elif resp.startswith(':tmi.twitch.tv'): # filters initial connection acks
      continue

    elif len(resp):
      username, channel, message = obj.parse_message(resp)
      print(f"Username: {username}\t Channel: {channel}\t Message: {message}\n")

      obj.check_for_raffle(message)
      
      # if (obj.count > 40) and (obj.elapsed_time > 80) and not obj.entered_raffle:
      if (obj.count > 10) and (obj.elapsed_time > 20) and not obj.entered_raffle:
        obj.enter_raffle()

    # Due to socket blocking, this will only run when a resp is received
    if obj.entered_raffle:
      obj.current_time = time.time()
      obj.elapsed_time = obj.current_time - obj.raffle_start_time
      
      # Has it been 15min since the raffle began?
      # If so, reset for next raffle
      if obj.elapsed_time > 60: 
      # if obj.elapsed_time > 900: # 15min
        obj.reset()

    obj.status()

### END main() ###

main()

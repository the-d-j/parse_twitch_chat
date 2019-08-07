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

 

  # pattern to match for username, channel, message
  reg = r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'

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
    self.count = 0
    self.responses = ["hey!", "yes!", "cool!", "bam!", "thanks!" "woohoo!", "ah yeah", "noice!", "sweet", "yup yup"]
  
    self.sock = socket.socket()
    self.sock.connect((self.server, self.port))

    self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
    self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
    self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))

    
  ### END INIT ###

  
  
  def status(self):
    print("Statuses:\nRAFFLE_STARTED:  {}\nENTERED_RAFFLE:  {}\nENTERED_RAFFLE_TIME:  {}\nRAFFLE_START_TIME:  {}\nCURRENT_TIME:  {}\nCOUNT:  {}\n"
      .format(self.raffle_started, self.entered_raffle, time.ctime(self.entered_raffle_time),
      time.ctime(self.raffle_start_time), time.ctime(self.current_time), self.count))

def main():
  signal.signal(signal.SIGINT, keyboardInterruptHandler)
  print("Press <CTRL+C> to end program and close sockets\n")

  g_bot = Bot(local_settings.TOKEN, local_settings.NICKNAME, local_settings.CHANNEL)
  while True:
    g_bot.status()
    time.sleep(2)

### END main() ###

main()

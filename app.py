#!/usr/bin/env python3

import rgem_gmail
import rgem_cam
from gpiozero import LED
from time import sleep

def main():
  to = "j54n1n+noreply@gmail.com"
  sender = "rgem1718+1@gmail.com"
  subject = "Rainerum Gemellaggio 2017/2018"
  msgHtml = "Hi<br/>Here is your picture !-)"
  msgPlain = "Hi\nHere is your picture !-)"
  # This is a comment.
  # Add your code below this comment and before if __name__ == '__main__':
  
  # First lets check if we have new emails for us.
  messages = rgem_gmail.NewMessages(sender)
  if len(messages) > 0:
    for message in messages:
      print(message)
  #rgem_gmail.SendMessage(sender, to, subject, msgHtml, msgPlain)
  #rgem_gmail.SendMessage(sender, to, subject, msgHtml, msgPlain, ["chip.png"])
  #rgem_cam.TakePicture()
  #rgem_gmail.NewMessages(sender)

if __name__ == '__main__':
  main()

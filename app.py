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
  
  # Create LED object on pin 14
  led = LED(14)
  
  # First lets check if we have new emails for us.
  messages = rgem_gmail.NewMessages(sender)
  if len(messages) > 0:
    # We have some messages.
    for message in messages:
      # Have we been asked to take a picture?
      msg_subject = message['Subject'].lower();
      if "take a pic" in msg_subject:
        # Take the picture and send it back.
        # Show the LED that we are doing something.
        led.on()
        pic = rgem_cam.TakePicture()
        to = message['From']
        subject = message['Subject']
        rgem_gmail.SendMessage(sender, to, subject, msgHtml, msgPlain, [ pic ])
        led.off()
        print("Sent a picture to: " + to)

if __name__ == '__main__':
  # Bonus: let the program run forever.
  while True:
    main()
    # Sleep for 30 seconds.
    sleep(30)

#!/usr/bin/env python3

import rgem_gmail
import rgem_cam

def main():
  to = "j54n1n+noreply@gmail.com"
  sender = "rgem1718+1@gmail.com"
  subject = "Test"
  msgHtml = "Hi<br/>Html Email"
  msgPlain = "Hi\nPlain Email"
  #rgem_gmail.SendMessage(sender, to, subject, msgHtml, msgPlain)
  #rgem_gmail.SendMessage(sender, to, subject, msgHtml, msgPlain, ["chip.png"])
  rgem_cam.TakePicture()
  #rgem_gmail.NewMessages(sender)

if __name__ == '__main__':
  main()

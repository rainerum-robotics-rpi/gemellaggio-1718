# MIT License
#
# Copyright (c) 2017 Julian Sanin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.utils import parseaddr
from email import encoders
from apiclient import errors, discovery
from pathlib import Path

SCOPES = 'https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Rainerum Gemellaggio 1718'

def get_credentials():
  """Gets valid user credentials from storage.
  
  If nothing has been stored, or if the stored credentials are invalid,
  the OAuth2 flow is completed to obtain the new credentials.
  
  To obtain the credentials file see also:
  https://developers.google.com/gmail/api/quickstart/python
  
  Returns:
    Credentials, the obtained credential.
  """
  #home_dir = os.path.expanduser('~')
  #credential_dir = os.path.join(home_dir, '.credentials')
  app_dir = str(Path(os.path.dirname(__file__)).parent)
  credential_dir = os.path.join(app_dir, 'credentials')
  if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
  credential_path = os.path.join(credential_dir, 'gmail-python-rgem1718.json')
  store = oauth2client.file.Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    #flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    client_secret_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
    try:
      flow = client.flow_from_clientsecrets(client_secret_path, SCOPES)
      flow.user_agent = APPLICATION_NAME
      credentials = tools.run_flow(flow, store)
      print("Storing credentials to " + credential_path)
    except:
      print("Could not access file " + client_secret_path)
  return credentials

def NewMessages():
  """Gets all unread messages.
  
  Returns:
    Messages, the obtained emails.
  """
  unread_emails = [ ]
  credentials = get_credentials()
  if not credentials or credentials.invalid:
    return unread_emails
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('gmail', 'v1', http=http)
  unread_msgs = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
  try: # do we have messages?
    unread_msgs['messages']
  except:
    print("No unread emails found. /\\_/\\ ") #  /\_/\
    print("                       ( o.o )")   # ( o.o )
    print("                        > ^ <")    #  > ^ <
    return unread_emails
  msgs_list = unread_msgs['messages']
  
  # See also: https://developers.google.com/gmail/api/v1/reference/users/messages#resource
  for msg in msgs_list:
    temp_dict = { }
    m_id = msg['id'] # get id of individual message
    message = service.users().messages().get(userId='me', id=m_id).execute()
    payld = message['payload'] # get payload of the message 
    hdr = payld['headers'] # get header of the payload
    
    for sbj in hdr: # getting the Subject
      if sbj['name'] == 'Subject':
        msg_subject = sbj['value']
        temp_dict['Subject'] = msg_subject
      else:
        pass
      
    for snd in hdr: # getting the Sender
      if snd['name'] == 'From':
        msg_from = snd['value']
        #temp_dict['Sender'] = msg_from
        addr_tuple = parseaddr(msg_from)
        temp_dict['From'] = addr_tuple[1] # Take email address part
      else:
        pass
       
    temp_dict['Snippet'] = message['snippet'] # fetching message snippet
    print (temp_dict)
    unread_emails.append(temp_dict) # This will create a dictonary item in the final list
       
    # This will mark the message as read
    #service.users().messages().modify(userId='me', id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute()
  return unread_emails

def SendMessage(sender, to, subject, msgHtml, msgPlain, files=[]):
  assert type(files)==list
  credentials = get_credentials()
  if not credentials or credentials.invalid:
    return
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('gmail', 'v1', http=http)
  if len(files) > 0:
    message1 = CreateMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, files)
  else:
    message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain)
  SendMessageInternal(service, "me", message1)

def SendMessageInternal(service, user_id, message):
  """Send an email message.
  
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me" can be used to
             indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def CreateMessage(sender, to, subject, msgHtml, msgPlain):
  #Create message container
  msg = MIMEMultipart('alternative') # needed for both plain & HTML (the MIME type is multipart/alternative)
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = to
  #Create the body of the message (a plain-text and an HTML version)
  msg.attach(MIMEText(msgPlain, 'plain'))
  msg.attach(MIMEText(msgHtml, 'html'))
  raw = base64.urlsafe_b64encode(msg.as_bytes())
  raw = raw.decode()
  body = {'raw': raw}
  return body

def CreateMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, files):
  ## An email with attachment is composed of 3 parts:
  # part 1: create the message container using a dictionary { to, from, subject }
  # part 2: attach the message_text with .attach() (could be plain and/or html)
   #part 3(optional): an attachment added with .attach()

  ## Part 1
  msg = MIMEMultipart() # when alternative: no attach, but only plain_text
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = to
  
  ## Part 2   (the message_text)
  # The order count: the first (html) will be use for email, the second will be attached
  # (unless you comment it)
  msg.attach(MIMEText(msgHtml, 'html'))
  #msg.attach(MIMEText(msgPlain, 'plain'))
  
  ## Part 3 (attachement) 
  # # to attach a text file you containing "test" you would do:
  # # message.attach(MIMEText("test", 'plain'))
  
  #-----About MimeTypes:
  # It tells gmail which application it should use to read the attachement (it acts like an extension for windows).
  # If you dont provide it, you just wont be able to read the attachement (eg. a text) within gmail. You'll have to download it to read it (windows will know how to read it with it's extension). 
  
  #-----3.1 get MimeType of attachment
  # option 1: if you want to attach the same file just specify it’s mime types
  # option 2: if you want to attach any file use mimetypes.guess_type(attached_file) 
  for file in files:
    my_mimetype, encoding = mimetypes.guess_type(file)
    # If the extension is not recognized it will return: (None, None)
    # If it's an .mp3, it will return: (audio/mp3, None) (None is for the encoding)
    # for unrecognized extension it set my_mimetypes to  'application/octet-stream'
    # (so it won't return None again). 
    if my_mimetype is None or encoding is not None:
      my_mimetype = 'application/octet-stream' 
    main_type, sub_type = my_mimetype.split('/', 1) # split only at the first '/'
    # if my_mimetype is audio/mp3: main_type=audio sub_type=mp3
    #-----3.2  creating the attachement
    # you don't really "attach" the file but you attach a variable that contains the
    # "binary content" of the file you want to attach
    # option 1: use MIMEBase for all my_mimetype (cf below)
    #  - this is the easiest one to understand
    # option 2: use the specific MIME (ex for .mp3 = MIMEAudio)
    #  - it's a shorcut version of MIMEBase
    # this part is used to tell how the file should be read and stored (r, or rb, etc.)
    if main_type == 'text':
      temp = open(file, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
      attachement = MIMEText(temp.read(), _subtype=sub_type)
      temp.close()
    elif main_type == 'image':
      temp = open(file, 'rb')
      attachement = MIMEImage(temp.read(), _subtype=sub_type)
      temp.close()
    elif main_type == 'application' and sub_type == 'pdf':   
      temp = open(file, 'rb')
      attachement = MIMEApplication(temp.read(), _subtype=sub_type)
      temp.close()
    else:                              
      attachement = MIMEBase(main_type, sub_type)
      temp = open(file, 'rb')
      attachement.set_payload(temp.read())
      temp.close()
    #-----3.3 encode the attachment, add a header and attach it to the message
    encoders.encode_base64(attachement)  # https://docs.python.org/3/library/email-examples.html
    filename = os.path.basename(file)
    attachement.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
    msg.attach(attachement)
 
  ## Part 4 encode the message (the message should be in bytes)
  msg_bytes = msg.as_bytes() # the message should converted from string to bytes.
  msg_base64 = base64.urlsafe_b64encode(msg_bytes) # encode in base64 (printable letters coding)
  raw = msg_base64.decode()  # need to JSON serializable (no idea what does it means)
  body = {'raw': raw}
  return body

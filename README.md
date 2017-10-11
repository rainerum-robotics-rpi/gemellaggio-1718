# Internet of Things with Raspberry Pi Cam

## Installation
Open a Terminal and execute following commands:
1. `sudo pip3 install --upgrade google-api-python-client`
2. `git clone https://github.com/rainerum-robotics-rpi/gemellaggio-1718.git`
3. `cd gemellaggio-1718`

## Execution
To run the app simply type:
* `./app.py`
If the application can not find a *.json* file you most likely have forgotten
to copy the credentials key file within the
[credentials folder](https://github.com/rainerum-robotics-rpi/gemellaggio-1718/tree/master/credentials).
Please add the keys as explained in the readme file of the credentials folder.

## Application Programming Interface (API)
Python 3.x is used to program this application. Checkout the docs:
* [Variables](https://docs.python.org/3/tutorial/introduction.html)
* [Flow controls (if, while, for)](https://docs.python.org/3/tutorial/controlflow.html)
* [Datastructures (lists, tuples, sets)](https://docs.python.org/3/tutorial/datastructures.html)
There exist two custom libraries that support your program. One is called
[rgem_gmail](https://github.com/rainerum-robotics-rpi/gemellaggio-1718/tree/master/rgem_gmail)
and the other one is called
[rgem_cam](https://github.com/rainerum-robotics-rpi/gemellaggio-1718/tree/master/rgem_cam).
Both are already inlcuded in the
[app.py](https://github.com/rainerum-robotics-rpi/gemellaggio-1718/blob/master/app.py)
file with the lines:
```
import rgem_gmail
import rgem_cam
```
Furthermore two other libraries are included with the lines:
```
from gpiozero import LED
from time import sleep
```
See also:
* [Basic Recipes - Gpiozero](https://gpiozero.readthedocs.io/en/stable/recipes.html)
* [time.sleep()](https://docs.python.org/3/library/time.html#time.sleep)

### Gmail Library
* `messages = rgem_gmail.NewMessages(address)` Checks out new messages sent to a certain address and marks them as read. The variable *message* contains a dictionary of received emails matching the specified *address*.
* `rgem_gmail.SendMessage(sender, to, subject, msgHtml, msgPlain, [ pic ])` Sends an email with given text and file attachments from given *sender* address to given *to* destination address. The attachment is a list with one or more filenames.

### Camera Library
* `pic = rgem_cam.TakePicture()` Takes a picture and saves it to with the filename as indicated by the return value variable *pic*.
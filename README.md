## Door Lock with Facial Recognition

### Setting up on Raspberry Pi
- https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826
- https://www.hackster.io/mjrobot/automatic-vision-object-tracking-5575c4
- https://www.hackster.io/mjrobot/pan-tilt-multi-servo-control-b67791
- https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
- https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

### Setting up on Ubuntu 18 Desktop
- Installing dependencies
```
sudo apt install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```
- Installing Pi Camera (https://www.youtube.com/watch?v=T8T6S5eFpqE)

### How to use lock.py
The lock.py controls the motors of the servo, PIR sensor, and push button.
```
- Still under construction -
```

### How to use pc_transmissions.py and pi_transmissions.py
The pi and pc are connected through sockets to send signal to open door
- Create two python scripts on the same directory level as pc_transmissions.py and pi_transmissions.py
- Copy the following snippet to the python scripts to run
- Run the script for pc first then script for pi
```
# pc script
from pc_transmissions import *
pc_node = PC_Node()
pc_node.signal_door_state('1')
pc_node.signal_motion()
```
```
from pi_transmissions import *
import time
pi_node = PI_Node()
pi_node.signal_door_state()
time.sleep(1)
pi_node.signal_motion("0")
```

### How to use generator.py script
The generator.py generates one time password. A qrcode is produced.
- Create a python script and ensure generator.py is on the same directory level
- Copy the following snippet to the python script to run
```
from generator import *
token = mkpassword()
print(token)
create_qr_code(token)
```

### How to use the password.py script
The password.py script sends the client.png and password.png to gmail. Email: islacchi.giftia@gmail.com Password: ubuntu123! (Expires on 20 Jan, 2019)
- Create a python script and ensure password.py is on the same directory level
- Copy the following snippet to the python script to run
```
from password import *
print("sending email")
owner = "Isla"
send_password = Password(owner)
send_password.run()
print("email sent")
```

### How to use the scanner.py script
The scanner.py checks whether the password tallys before opening the door
- Create a python script and ensure scanner.py is on the same directory level
- Copy the following snippet to the python script to run
```
from scannner import *
password = "1234567890"
qrscanner = QRScanner(password)
open_door = qrscanner.run()
if open_door:
    print("open door")
else:
    print("close door")
```

### How to use the internet.py script
The internet.py checks the internet connection before opening the door
- Create a python script and ensure internet.py is on the same directory level
- Copy the following snippet to the python script to run
```
from internet import *
response = test_internet_connectivity()
if response == 0:
    print(hostname + " is up")
else:
    print(hostname + " is down")
```

### How to use the camera.py script
The camera.py starts up the camera for 5 seconds and check if the face belongs to one of the owners. A client.png image is produced.
- Store all the owner faces in the images directory
- Go to camera.py and update the dictionary constants_name to map the name of owner to image
- Create a python script and ensure camera.py is on the same directory level
- Copy the following snippet to the python script and run
```
from camera import *
get_owner_image_encoding()                  # get the image encoding of the owners
camera = Camera()                           # create an instance of the variable
open_door_data = camera.run()               # return a tuple - the first is the name of the owner 
                                            # and second is a boolean whether the door should be open 
if open_door_data[1]:
    print("door is opening")
    print("Welcome " + open_door_data[0])
else:
    print("door will not open")
```

### Others
- dev.py is for testing


### References
- https://www.gadgetdaily.xyz/create-css3-folding-caption-effects/
- https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/
- https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826
- https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
- https://www.youtube.com/watch?v=T8T6S5eFpqE
- https://nitratine.net/blog/post/how-to-send-an-email-with-python/?utm_source=pythonanywhere&utm_medium=redirect&utm_campaign=pythonanywhere_organic_redirect
- http://code.activestate.com/recipes/578169-extremely-strong-password-generator/
- https://realpython.com/python-sockets/
- https://realpython.com/python-sockets/
- https://stackabuse.com/basic-socket-programming-in-python/
- https://pythonspot.com/python-network-sockets-programming-tutorial/

### Team Members
- Brandon Ng https://github.com/nwjbrandon
- Nishanth Elango https://github.com/nishanthelango
- Paul Tho https://github.com/dragontho
- Ng Jing Kiat https://github.com/muserr

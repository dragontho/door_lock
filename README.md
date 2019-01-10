## Door Lock with Facial Recognition

### Project Description
The door is designed to open when the owner's face and one-time password is verified. When the PIR 
sensor detects a person is approaching, the camera turns on. If the owner's face is recognized, a 
password is generated and sent to the owner's gmail in QR code to scan. The camera does the 
verfication real-time. The servo turns, and the door opens for the owner to enter

### Running the code on Raspberry Pi
- Follow the instructions below
    - https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
    - https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65
- Install Python Pacakages
```
pip3 install -r requirements.txt
```
- Set the path variable that connects the virtual environment to the system's python packages 
- To run the python scripts
```
source ./.profile
workon cv
export PYTHONPATH=$PYTHONPATH=/usr/lib/python3.5/dist-packages:/usr/local/lib/python3.5/dist-packages:/usr/lib/python3/dist-packages
cd ./code_for_pi
python3 main.py
```

### Running the code on Ubuntu 18
- Install Python Pacakages
```
sudo apt install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```
- To run the python scripts
```
cd ./code_for_pc
python3 main.py
```

### How to use lock.py
The lock.py controls the motors of the servo, PIR sensor, and push button.
- Make connections to pins
    - Motor: 7
    - LED 1: 13
    - LED 2: 15
    - PIR Sensor: 37
```
python3 lock.py
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
get_owner_image_encoding()                  
camera = Camera()                          
open_door_data = camera.run()              
if open_door_data[1]:
    print("door is opening")
    print("Welcome " + open_door_data[0])
else:
    print("door will not open")
```

### References
- https://www.gadgetdaily.xyz/create-css3-folding-caption-effects/
- https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/
- https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
- https://www.youtube.com/watch?v=T8T6S5eFpqE
- https://nitratine.net/blog/post/how-to-send-an-email-with-python/?utm_source=pythonanywhere&utm_medium=redirect&utm_campaign=pythonanywhere_organic_redirect
- http://code.activestate.com/recipes/578169-extremely-strong-password-generator/
- https://realpython.com/python-sockets/
- https://realpython.com/python-sockets/
- https://stackabuse.com/basic-socket-programming-in-python/
- https://pythonspot.com/python-network-sockets-programming-tutorial/
- https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826
- https://www.hackster.io/mjrobot/automatic-vision-object-tracking-5575c4
- https://www.hackster.io/mjrobot/pan-tilt-multi-servo-control-b67791

### Team Members
- Brandon Ng https://github.com/nwjbrandon
- Nishanth Elango https://github.com/nishanthelango
- Paul Tho https://github.com/dragontho
- Ng Jing Kiat https://github.com/muserr

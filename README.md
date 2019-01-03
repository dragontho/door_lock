## Door Lock with Facial Recognition

### Setting up
```
sudo apt install virtualenv
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
python3 camera.py
```

### How to use the camera script
- Store all the owner faces in the images directory
- Go to camera.py and update the dictionary constants_name to map the name of owner to image
- Create a python script and ensure camera.py is on the directory level
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


### References
- https://www.gadgetdaily.xyz/create-css3-folding-caption-effects/
- https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/
- https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826


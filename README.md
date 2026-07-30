# Hand recognition ball bouncer
(creative name i know) program that tracks two hands using the camera and mediapipe. drawing a bar between the tips of both index fingers. when an on screen ball hits the line it bounces off so kinda like pong <br>This program was made because i wanted to test out object recognition and know how to use it so it is a little demo i made showcasing it.

## Demo of program

im yet to put an image and video here


## Make changes yourself
this is for mac devices with brew installed, if brew is not installed refer to [HomeBrew Install Docs](https://github.com/Homebrew/install "@Homebrew git") to install brew.

### install python version 3.11
It is mandatory your using python 3.11 or below otherwise mediapipe wont work

```
brew install python@3.11
```

### setup and activate vinv

```
python3.11 -m venv venv
source venv/bin/activate
```

### install dependecies

```
pip install --upgrade pip
pip install mediapipe opencv-python
```

## Build yourself
This compiling uses nuitka due to its nature it takes quite a while.
This is for Mac devices.

### installing nuitka
```
pip install nuitka
```
### Building main.app
```
python -m nuitka --standalone --macos-create-app-bundle --enable-plugin=numpy --include-package=mediapipe --include-package=cv2 --include-package-data=mediapipe main.py
```
### add camera permitions

open the ```Info.plist``` file

```
open -e main.app/Contents/Info.plist
```

Add these two lines before ```</dict>```
```
<key>NSCameraUsageDescription</key>
<string>This app needs camera access for hand and face tracking.</string>
```
These lines are just in case for the camera permissions because MacOS can be weird about camera permitions sometimes

### resign the app file
because we modified ```Info.plist``` The app wont open because the signature is no longer valid from our edits.
```
codesign --force --deep --sign - main.app
```

### open ```main.app```

either double click the application made called ```main``` or:
```
open main.app
```
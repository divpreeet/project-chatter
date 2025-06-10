# chatter - your personal AI voice assistant
> aka project-chatter, a project for [shipwrecked](https://shipwrecked.hackclub.com) by hackclub!

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.1-brightgreen.svg)

## table of contents
for the main stuff:

- [how to install chatter](#how-to-install-chatter-from-source)
- [troubleshooting errors](#troubleshooting)
- [usage](#usage)
- [privacy](#privacy)

## what is chatter?
![chatter_screenshot](assets/speaking.png)
chatter is AI voice assistant made purely in python, from the UI, to the voice recognition, all made in python! chatter uses the [hackclub ai](https://ai.hackclub.com/) for responses!


## how to install chatter?
i plan on releasing a standalone app for chatter for macos, windows and linux! but thats still a WIP, until you can run chatter from source!


## how to install chatter from source
### Requirements
- Python 3.9 or newer
- pip
- A working microphone (set as default for now)
- An internet connection

### Installation
```
git clone https://github.com/divpreeet/project-chatter.git
cd project-chatter
```
### Create a python venv (recommended)
```
python3 -m venv venv
```

#### On Windows 
```
venv\Scripts\Activate
```
#### On macOS or Linux
```
source venv/bin/activate
```

then install deps using
```
pip install -r requirements.txt
```
### Install other deps (according to OS)

#### Windows
no extra steps! you're good to go!

#### macOS
install portaudio
```
brew install portaudio
```
#### Linux
install portaudio dev headers and pyaudio
```
sudo apt-get install portaudio19-dev python3-pyaudio
```

### Run!
just run chatter using
```
cd main
python3 main.py
```
> if your using macOS run from the default terminal and allow Microphone Privelleges!

## usage
it's simple! just say 'chatter' along your message and chatter would respond!
extra stuff:
- you can also just say chatter, without saying your message, that would make chatter say 'Yes?' after which you could continue asking your message
- saying stuff like 'chatter goodbye' or anything from bye, goodbye, exit, quit, along with 'chatter' simply exits the appication
- try saying 'chatter what are you up to' for a surprise
- if your hacky and want ultimate customization, just open up the main.py and adjust the stuff that you'd want! like the wake words, end words and so on! i hope the code is readable 😭


## troubleshooting
- Ensure your microphone is connected and set as the default input device.
- If you encounter errors related to audio or microphone access, make sure PortAudio is installed and all Python dependencies are satisfied.
- also sometimes chatter might not hear you, due to ambient noise or your microphone!

## privacy
chatter doesnt store any data, not from your voice or computer, it simply just puts together multiple python libraries and has a nice UI, no shady stuff under the hood!

## extra project screenshots
![goodbye](assets/goodbye.png)
![yes](assets/yes.png)
![idle](assets/idle.png)
![speaking](assets/speaking.png)
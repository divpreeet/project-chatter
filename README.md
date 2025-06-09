# chatter - your personal AI voice assistant
> aka project-chatter, a project for [shipwrecked](https://shipwrecked.hackclub.com) by hackclub!

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.1-brightgreen.svg)

## what is chatter?
chatter is AI voice assitant made purely in python, from the UI, to the voice recognition, all made in python! chatter uses the hackclub ai for responses!

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
python3 -m venv venv

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
python3 main.py
```
> if your using macOS run from the default terminal and allow Microphone Privelleges!

## troubleshooting
- Ensure your microphone is connected and set as the default input device.
- If you encounter errors related to audio or microphone access, make sure PortAudio is installed and all Python dependencies are satisfied.

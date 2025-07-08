# chatter - your personal AI voice assistant
> aka project-chatter!

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.1-brightgreen.svg)

## table of contents
for the main stuff:

- [how to install chatter](#how-to-install-chatter-from-source)
- [troubleshooting errors](#troubleshooting)
- [usage](#usage)
- [customization](#customization)
- [privacy](#privacy)

## what is chatter?
![chatter_screenshot](assets/speaking.png)
chatter is AI voice assistant made purely in python, from the UI, to the voice recognition, all made in python! chatter uses the [hackclub ai](https://ai.hackclub.com/) for responses! chatter uses local models for the tts and speech!


## how to install chatter?
i plan on releasing a standalone app for chatter for macos, windows and linux! but thats still a WIP, until then you can run chatter from source!


## how to install chatter from source
### install `uv` 
> **Note:** project-chatter currently doesnt work on windows, due to ```piper-phoenimze``` packages not supporting it.


#### linux (all distros) & macOS
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### install Python 3.12 using `uv`
```sh
uv python install 3.12
```
this downloads and manages Python 3.12 locally for your projects.

### clone the repository
```sh
git clone https://github.com/divpreeet/project-chatter.git
cd project-chatter
```

### create a virtual environment with Python 3.12
```sh
uv venv --python 3.12
source .venv/bin/activate
```

### install system dependencies

#### Ubuntu/Debian
```sh
sudo apt update
sudo apt install -y build-essential portaudio19-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-dev
```

#### Fedora
```sh
sudo dnf install -y gcc python3-devel portaudio-devel SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel freetype-devel libffi-devel libsndfile-devel
```

#### Arch Linux
```sh
sudo pacman -Syu --needed python portaudio sdl2 sdl2_image sdl2_mixer sdl2_ttf freetype2 libffi libsndfile
```

### install Python dependencies
```sh
uv pip install -r requirements.txt
```

### run Chatter!
```sh
python main/chatter.py
```

#### note:
- On macOS, run from the default Terminal and allow Microphone access when prompted.
- On Linux, if you have audio permission issues, ensure your user is in the `audio` group.
- If you see errors about `piper-phonemize`, make sure your `requirements.txt` uses `piper-phonemize-cross` as described in troubleshooting.

---


## usage
it's simple! just say 'chatter' along your message and chatter would respond!
extra stuff:
- you can also just say chatter, without saying your message, that would make chatter say 'Yes?' after which you could continue asking your message
- saying stuff like 'chatter goodbye' or anything from bye, goodbye, exit, quit, along with 'chatter' simply exits the appication
- try saying 'chatter what are you up to' for a surprise
- if your hacky and want ultimate customization, just open up the main.py and adjust the stuff that you'd want! like the wake words, end words and so on! i hope the code is readable 😭

## customization
you can also customize the look and feel for chatter! 

### looks
just open the [config file](main/config.json) and mess with it however you want! its in simple rgb colors, and you can change everything you see!

here are some templates! to use them just copy paste the code into the file!

```jsonc
{
  "theme": "default",
  "bg_color": [23, 23, 23],
  "eye_color": [217, 217, 217],
  "tip_color": [180, 180, 180],
  "fonts": {
    "caption": "Inter.ttf",
    "caption_size": 28,
    "tip_size": 18
  },
  "tip_interval": 20
}
```

```jsonc
{
  "theme": "latte",
  "bg_color": [239, 241, 245],
  "eye_color": [76, 79, 105],
  "tip_color": [108, 111, 133],
  "fonts": {
    "caption": "Inter.ttf",
    "caption_size": 28,
    "tip_size": 18
  },
  "tip_interval": 20
}

```

```jsonc
{
  "theme": "frappe",
  "bg_color": [35, 38, 52],
  "eye_color": [115, 121, 148],
  "tip_color": [165, 173, 203],
  "fonts": {
    "caption": "Inter.ttf",
    "caption_size": 28,
    "tip_size": 18
  },
  "tip_interval": 20
}

```

```jsonc
{
  "theme": "macchiato",
  "bg_color": [36, 39, 58],
  "eye_color": [110, 115, 141],
  "tip_color": [184, 192, 224],
  "fonts": {
    "caption": "Inter.ttf",
    "caption_size": 28,
    "tip_size": 18
  },
  "tip_interval": 20
}

```
```jsonc
{
  "theme": "mocha",  
  "bg_color": [30, 30, 46],
  "eye_color": [152, 139, 162],
  "tip_color": [166, 173, 200],
  "fonts": {
    "caption": "Inter.ttf",
    "caption_size": 28,
    "tip_size": 18
  },
  "tip_interval": 20
}
```

these are just some templates, feel free to add on!

### wake + end words
you can customize the wake and end words too! instead of `chatter` you could make it `bob`, simply open the [main.py](main/main.py) and change the `WAKE_WORDS` and `END_WORDS` to whatever you want

from:
```python
WAKE_WORDS = ["chatter", "charter", "chadar", "chadda"]
END_WORDS = ["bye", "goodbye", "exit", "quit"]
```

to:
```python
WAKE_WORDS = ["bob", "bop"]
END_WORDS = ["quiet", "shut up"]
```


## troubleshooting
- Ensure your microphone is connected and set as the default input device.
- If you encounter errors related to audio or microphone access, make sure PortAudio is installed and all Python dependencies are satisfied.
- also sometimes chatter might not hear you, due to ambient noise or your microphone!
- also make sure you first `cd main` or the equivalent for windows before running `chatter.py`
- double-check you installed all system dependencies for your OS.
- use the recommended Python version (3.12), and use `uv` for faster, more reliable installs.
- still have an issue? copy the error and open an issue.

## privacy
chatter doesnt store any data, not from your voice or computer, it simply just puts together multiple python libraries and has a nice UI, no shady stuff under the hood!

## extra project screenshots
![goodbye](assets/goodbye.png)
![yes](assets/yes.png)
![idle](assets/idle.png)
![speaking](assets/speaking.png)

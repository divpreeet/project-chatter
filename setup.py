from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent

long_description = (here / "README.md").read_text(encoding="utf-8")
raw_reqs = (here / "requirements.txt").read_text().splitlines()
install_requires = [
    r for r in raw_reqs
    if r and not (r.startswith("piper-phonemize") or r.startswith("piper-tts"))
]

setup(
    name="project-chatter",
    version="0.1.1",
    author="Divpreet Singh",
    author_email="ytbraced@gmail.com",
    description="Chatter — AI Voice Assistant with Pygame UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divpreeet/project-chatter",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "voice": [
            "piper-phonemize-cross>=1.2.1",
            "piper-tts==1.2.0"
        ]
    },
    include_package_data=True,
    package_data={
        "main": [
            "models/UK/en_GB-northern_english_male-medium.onnx",
            "models/UK/en_GB-northern_english_male-medium.onnx.json",
            "Inter.ttf"
        ]
    },

    entry_points={
        "console_scripts": [
            "chatter-start=main.chatter:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio"
    ],
)

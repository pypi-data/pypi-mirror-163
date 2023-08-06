pi-door-buzz
=======

[![Python package](https://github.com/nikhiljohn10/pi-door-buzz/workflows/Python%20package/badge.svg?branch=master)](https://pypi.python.org/pypi/pi-door-buzz/)
[![Latest Version](https://img.shields.io/pypi/v/pi-door-buzz)](https://pypi.python.org/pypi/pi-door-buzz/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pi-door-buzz)](https://pypi.python.org/pypi/pi-door-buzz/)
[![Code Size](https://img.shields.io/github/languages/code-size/nikhiljohn10/pi-door-buzz)](https://pypi.python.org/pypi/pi-door-buzz/)
[![Downloads](https://img.shields.io/pypi/dm/pi-door-buzz)](https://pypi.python.org/pypi/pi-door-buzz/)
[![License](https://img.shields.io/pypi/l/pi-door-buzz)](https://github.com/nikhiljohn10/pi-door-buzz/blob/master/LICENSE)

A python package for door buzz detection

Visit Official documentation at [pi-door-buzz.nikz.in](https://pi-door-buzz.nikz.in/)

### Platforms Supported

* Raspberry Pi
* Linux
* MacOS

### Hardware Requirements

* Raspberry Pi (optional)
* Bread Board (optional)
* Microphone
* Audio Card (Needed for analog microphones with a jack)

### Dependencies

* [Python 3.6+](https://docs.python.org/3/)
* [gpiozero](https://gpiozero.readthedocs.io)
	* [RPi.GPIO](https://pypi.org/project/RPi.GPIO)
* [PyAudio](https://pypi.org/project/PyAudio)
	* [PortAudio](http://www.portaudio.com/) (Need to be installed manually)
	* Audio Driver (Automatically loaded by OS after a restart)
* [Munch](https://pypi.org/project/munch/)

### Upcoming features

* Adding advanced door buzz detection algorithms
* Adding support for automation platforms like Amazon Alexa, Google Home, IFTTT etc.

### Development

```
git clone https://github.com/nikhiljohn10/pi-door-buzz
cd pi-door-buzz
make help # Display the possible options available
```

Version number is fetched from [`pidoorbuzz/__init__.py`](https://github.com/nikhiljohn10/pi-door-buzz/blob/master/pidoorbuzz/__init__.py)

- Package - [/pidoorbuzz](https://github.com/nikhiljohn10/pi-door-buzz/tree/master/pidoorbuzz)
- Examples - [/example](https://github.com/nikhiljohn10/pi-door-buzz/tree/master/example)
- Documentation - [/docs/source](https://github.com/nikhiljohn10/pi-door-buzz/tree/master/docs/source)
- Test Cases - [/test](https://github.com/nikhiljohn10/pi-door-buzz/tree/master/tests)
- Github Actions - [/.github/workflows](https://github.com/nikhiljohn10/pi-door-buzz/tree/master/.github/workflows)

### License

[MIT License](https://github.com/nikhiljohn10/pi-door-buzz/blob/master/LICENSE)

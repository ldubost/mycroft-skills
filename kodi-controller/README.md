# Kodi Remote Control Skill for Mycroft

## Description
Mycroft skill to provide integration to Kodi (XBMC). Enables
the user to Play or Pause the currently playing video via voice
commands made to mycroft.

This code is based on the mycroft-skill-kodi from k3yb0ardn1nja
https://github.com/k3yb0ardn1nja/mycroft-skill-kodi
which did not work in the third party skill directory

## Setup
1. Enable Web Server for remote control in Kodi's System Settings.
    - [Enabling Web Server](http://kodi.wiki/view/Settings/Services#Webserver)
    - Do not use a password
    - Use port (8080)
    - Or copy kodi-config.json to mycroft/configuratio/kodi-config.json and edit the file to set the proper server, port and credentials

2. Copy or clone this repository into mycroft's third party skills directory

## Usage
#### Examples:

    "mycroft, play the movie"
    "mycroft, play the video"
    "mycroft, pause the movie"
    "mycroft, pause the video"
    "mycroft, stop the movie"
    "mycroft, stop the video"
    "mycroft, close the movie"
    "mycroft, close the video"
    "mycroft, end the movie"
    "mycroft, end the video"

## LICENCE

This directory is double licenced under GPL or under the original licence

## OLD LICENCE:

Copyright (c) 2016, k3yb0ardn1nja k3yb0ardn1nja@gmail.com

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

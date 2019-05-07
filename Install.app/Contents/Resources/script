#!/bin/bash

if [ $SUDO_USER ]; then 
    USERNAME=$SUDO_USER 
else USERNAME=`whoami` 
fi

PATH_LOCAL="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
app_path="$PATH_LOCAL/TubZel.app"
cfg_path="$PATH_LOCAL/tubzel.cfg"

cp -R $app_path "/Applications/TubZel.app"
cp $cfg_path "/Users/$USERNAME/tubzel.cfg"

open ~/tubzel.cfg -a TextEdit
open -a TubZel

# Add to Login Items
items=`osascript -e 'tell application "System Events" to get the name of every login item'`

if [[ ! $items == *"TubZel"* ]]; then
  osascript -e 'tell application "System Events" to make new login item with properties { path: "/Applications/TubZel.app" } at end'
fi

exit 0
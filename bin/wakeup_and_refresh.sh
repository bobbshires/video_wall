#!/bin/bash
#
# reload_current_page.sh
# script to reload current page, suitable for cronjobs

osascript -e 'delay 8.0' -e 'tell application "Google Chrome" to tell the active tab of window 1 to reload'

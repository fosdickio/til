# Troubleshooting Captive Portal Wifi Issues

This document provides some potential troubleshooting options that can aid in resolving issues with the wifi captive portal not opening on a Mac when connecting to a public wifi network.

## Option #1: Access Default Captive Addresses

Try accessing the following URLs/IPs to access the acceptance/login screen:

1. captive.apple.com
2. 192.168.1.1
3. 127.1.1.1

## Option #2: Launch Captive Network Assistant

Connect to the public wifi network then force the Captive Network Assistant app to start.

```bash
sudo /System/Library/CoreServices/Captive\ Network\ Assistant.app/Contents/MacOS/Captive\ Network\ Assistant
```

## Option #3: Check System Launch Folders

Check the following system launch folders for anything that might be causing a conflict:

1. `/Library/LaunchAgents/`
2. `/Library/LaunchDaemons/`

You can then disable each service in the override database by using `sudo launchctl unload ${FILE_PATH}` and then removing it.

## Option #4: Safe Boot

Shut down the computer and wait 10 seconds. After this, boot into safe mode by turning the computer on and holding down the `SHIFT` key until the login appears. Login, connect to the wifi, and then reboot out of safe mode.

## Option #5: Remove Custom DNS Servers

Remove existing DNS servers from your DNS preferences (System Preferences > Network > Advanced > DNS).

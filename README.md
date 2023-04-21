# gardena_smart

This is a node-red / MQTT integration for Gardena Sileno Smart and similar Autmowers, based on the Husquarna API.

Technically, other gardena smart devices should work too, but I can not test that.

My installation is on a linux machine, so this document refers to Linux (tested on RPI3B+ and Intel NUC, running Debian 11.)  

**Update 04/23**  
Due to some changes, my API key got blocked, because the restart was too fast (I assume), which was caused by the websocket connection raising errors ever few minutes.
I have now implemented a propper reconnect for the websocket, so it seems no longer required to restart the service itself.

**How to install:**
Download GardenaSmart.py and place it somewhere in your user directory.
Register at Husqvarna and get yourself an API Key:
https://developer.husqvarnagroup.cloud/docs/get-started

Edit the User/Passwords/Settings lines where indicated
Make sure you have the Python dependencies installed on your machine:
pip install websocket
pip install websocket-client
pip install paho-mqtt
pip install requests
pip install json

Create a systemd service for the program.
If you don't know how to create a systemd service, there's a pletheora of howTo's out there like 
https://linuxhandbook.com/create-systemd-services/

Import the attached sample Flow in Node-Red and adjust MQTT Broker etc to yours. This flow integrates with domoticz, but it should be easy to interface to any other HA-system, as long as it understands MQTT (if your's doesn't, it is most likely crap anyway).

I have this running for 3 years now, sometimes they make unexpected changes to the API.
For now it works as is.

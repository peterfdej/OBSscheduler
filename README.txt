OBSsceduler can be used as a sceduled scene switcher for OBS.
It uses the OBS-websocket plugin by Palakis.

You need to run obssceduler.py in python.
Python uses websocket-client (pip install websocket-client)

Edit obshost.xml for connect to the OBS server.
Host is the ip address of the OBS server.
The default port is 4444.
It is recommended to use a password for the OBS-websocket API.

obssceduletimes.xml is used for the times (date and time, format DDMMYYYYHHmmss) you want to switch scene, the scene name en the transition type.
The label processed need to be 0, until scene is switched, it will set to 1.

Every hour it wil create JSON files containing scene and transition information of your OBS  server.

For the mysql (MariaDB) version python uses mysql-connection-python (pip install mysql-connection-python).


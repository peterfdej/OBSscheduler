OBSscheduler can be used as a scheduled scene and sources switcher for OBS.
There are 3 parts:
- mySQL database OBSdb
- python script obsschedulermySQL.py
- webapplication for add/editing schedule rules.

In OBS you need the OBS-websocket plugin by Palakis.

You need to run obsschedulermySQL.py in python.
Python uses websocket-client (pip install websocket-client)
and mysql connector (pip install mysql-connector-python)

Edit obsschedulermySQL.py for connection to mySQL

Edit 'host' table in obsdb for connect to the OBS server.
Hostname is the ip address of the OBS server.
The default port is 4444.
It is recommended to use a password for the OBS-websocket API.

Edit database_connection.php for connection to mySQL database.


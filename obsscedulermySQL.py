#!/usr/bin/env python

import sys
import time
import socket
import websocket
import hashlib
import base64
import json
import mysql.connector
from mysql.connector import Error
try:
    import thread
except ImportError:
    import _thread as thread



mysqlconfig = {
  'user': 'user',
  'password': 'pass',
  'host': '127.0.0.1',
  'port': '3307',
  'database': 'OBSdb',
  'raise_on_warnings': True
}

try:
	connection = mysql.connector.connect(**mysqlconfig)
	if connection.is_connected():
		db_Info = connection.get_server_info()
		print("Connected to MySQL Server version ", db_Info)
		mycursor = connection.cursor(dictionary=True)
		mycursor.execute("SELECT * FROM host")
		records = mycursor.fetchall()
		for row in records:
			host = row["hostname"]
			port = row["port"]
			password = row["pass"]

except Error as e:
	print("Error while connecting to MySQL", e)

StudioMode = False
exporttime = '1500' # every hour at mmss
GetAuthRequired = {"request-type" : "GetAuthRequired" ,"message-id" : "1"};
GetStudioModeStatus = {"request-type" : "GetStudioModeStatus" , "message-id" : "GetStudioModeStatus"}
GetSceneList = {"request-type" : "GetSceneList" , "message-id" : "getSceneList"}
GetTransitionList = {"request-type": "GetTransitionList","message-id" : "GetTransitionList"}

while True:
	try:
		def on_message(ws, message):
			data = json.loads(message)
			#print (data["message-id"])
			#print (data)
			if "error" in data:
				if (data["error"] == "Authentication Failed."):
					print("Authentication Failed.")
					ws.keep_running = False
				else:
					print (data)
			elif "message-id" in data:
				if (data["message-id"] == "GetStudioModeStatus"):
					global StudioMode
					StudioMode = data["studio-mode"]
				elif (data["message-id"] == "getSceneList"):
					mycursor = connection.cursor()
					mycursor.execute("TRUNCATE TABLE scenenames")
					connection.commit()
					for i in data['scenes']:
						scene = i['name']
						mycursor = connection.cursor()
						qry = "INSERT INTO scenenames(scene) VALUES('" + scene + "')"
						mycursor.execute(qry)
						connection.commit()
				elif (data["message-id"] == "GetTransitionList"):
					mycursor = connection.cursor()
					mycursor.execute("TRUNCATE TABLE transitionnames")
					connection.commit()
					for i in data['transitions']:
						trans_type = i['name']
						mycursor = connection.cursor()
						qry = "INSERT INTO transitionnames(transition) VALUES('" + trans_type + "')"
						mycursor.execute(qry)
						connection.commit()
				elif (data["authRequired"]):
					print("Authentication required")
					secret = base64.b64encode(hashlib.sha256((password + data['salt']).encode('utf-8')).digest())
					auth = base64.b64encode(hashlib.sha256(secret + data['challenge'].encode('utf-8')).digest()).decode('utf-8')
					auth_payload = {"request-type": "Authenticate", "message-id": "2", "auth": auth}
					ws.send(json.dumps(auth_payload))
				else:
					print(data)
			elif "update-type" in message:
				if (data["update-type"] == "StudioModeSwitched"):
					StudioMode = data["new-state"]

		def on_error(ws, error):
			print(error)
			ws.close()

		def on_close(ws):
			print("Connection error.")
			ws.keep_running = False
			time.sleep(30)

		def on_open(ws):
			def run(*args):
				ws.send(json.dumps(GetAuthRequired))
				time.sleep(2)
				if ws.sock:
					ws.send(json.dumps(GetStudioModeStatus))
					while True:
						currentdtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
						mycursor = connection.cursor(dictionary=True)
						mycursor.execute("SELECT * FROM scedules Where processed = 0")
						records = mycursor.fetchall()
						print(time.strftime("%H:%M:%S",time.localtime()))
						for row in records:
							dtime = row["dtime"]
							scene = row["scene"]
							trans_type = row["transition"]
							if currentdtime == dtime:
								message={"request-type" : "SetCurrentTransition" , "message-id" : "SetCurrentTransition" ,"transition-name":trans_type};
								ws.send(json.dumps(message))
								message = {"request-type" : "SetCurrentScene" , "message-id" : "SetCurrentScene" , "scene-name" : scene};
								ws.send(json.dumps(message))
								mycursor = connection.cursor()
								qry = "UPDATE scedules SET processed = 1 WHERE dtime = '" + dtime + "'"
								mycursor.execute(qry)
								connection.commit()
								print("Transition to: " + scene + " at " + time.strftime("%H:%M:%S",time.localtime()))
						time.sleep(0.5) #no need 100's loops a second
						# export scene names and transition names.
						timenow = time.strftime("%M%S",time.localtime())
						if timenow == exporttime:
							ws.send(json.dumps(GetSceneList))
							ws.send(json.dumps(GetTransitionList))
							time.sleep(1) #prevent multiple exports
			thread.start_new_thread(run, ())

		if __name__ == "__main__":
			#websocket.enableTrace(True)
			ws = websocket.WebSocketApp("ws://{}:{}".format(host, port),on_message = on_message,on_error = on_error,on_close = on_close)
			ws.on_open = on_open
			ws.run_forever()

	except Exception:
		print("Connection error")
		time.sleep(10)





